import threading
import requests
from collections import defaultdict

# Конфигурация
URL = "http://localhost:8000/coffee/"
NUM_THREADS = 20
REQUESTS_PER_THREAD = 20
TOTAL_REQUESTS = NUM_THREADS * REQUESTS_PER_THREAD

# Глобальная статистика
stats = defaultdict(int)
stats_lock = threading.Lock()


def make_requests(thread_id):
    for i in range(REQUESTS_PER_THREAD):
        try:
            response = requests.get(URL)
            content = response.text

            with stats_lock:
                if "Я кинйач" in content:
                    stats["reversed"] += 1
                else:
                    stats["normal"] += 1

        except Exception:
            with stats_lock:
                stats["errors"] += 1


if __name__ == "__main__":
    # Создаем и запускаем потоки
    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=make_requests, args=(i,))
        threads.append(t)
        t.start()

    # Ждем завершения всех потоков
    for t in threads:
        t.join()

    # Выводим статистику
    print(f"\nTotal requests: {TOTAL_REQUESTS}")
    print(f"Successful responses: {stats['normal'] + stats['reversed']}")
    print(
        f"Reversed responses: {stats['reversed']} ({(stats['reversed'] / TOTAL_REQUESTS) * 100:.1f}%)"
    )
    print(f"Errors: {stats['errors']}")

    # Проверяем счетчик
    expected_reversed = TOTAL_REQUESTS // 10
    print(f"\nExpected reversed responses: {expected_reversed}")
    print(f"Actual reversed responses: {stats['reversed']}")
    print(
        "Status:",
        "PASSED" if stats["reversed"] == expected_reversed else "FAILED",
    )
