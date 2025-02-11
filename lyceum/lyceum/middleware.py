import re
import threading


class ReverseRussianWordsMiddleware:
    response_count = 0
    lock = threading.Lock()  # Блокировка для потокобезопасности

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .settings import get_allow_reverse  # Локальный импорт

        # Получаем ответ ДО увеличения счетчика
        response = self.get_response(request)

        # Увеличиваем счетчик только если ALLOW_REVERSE=True
        if get_allow_reverse():
            with self.lock:  # Атомарное увеличение
                self.__class__.response_count += 1
                current_count = self.__class__.response_count

            # Переворачиваем слова каждые 10 запросов
            if current_count % 10 == 0:
                self._reverse_content(response)

        return response

    def _reverse_content(self, response):
        """Переворачивает русские слова в контенте."""
        content_type = response.get("Content-Type", "")
        if "text" in content_type or content_type == "":
            try:
                content = response.content.decode("utf-8")
            except UnicodeDecodeError:
                return

            reversed_content = re.sub(
                r"\b[а-яА-ЯёЁ]+\b",  # Только целые слова
                lambda m: m.group(0)[::-1],
                content,
            )
            response.content = reversed_content.encode("utf-8")
