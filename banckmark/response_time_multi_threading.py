import requests
import time
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed



def measure_GET_response_time(url):
    start_time = time.perf_counter()
    try:
        response = requests.get(url)
        end_time = time.perf_counter()

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        return (end_time - start_time) * 1000
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def average_response_time_for_GET(url, num_requests):
    response_times = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(measure_GET_response_time, url) for _ in range(num_requests)]

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                response_times.append(result)

    if not response_times:
        print("No successful requests.")
        return None, None, None

    average_time = sum(response_times) / len(response_times)
    min_time = min(response_times)
    max_time = max(response_times)

    plt.plot(range(1, len(response_times) + 1), response_times, marker='o', color='b', label="Timp de raspuns (ms)")
    plt.axhline(y=average_time, color='r', linestyle='--', label=f"Media: {average_time:.2f} ms")
    plt.axhline(y=min_time, color='g', linestyle='--', label=f"Minim: {min_time:.2f} ms")
    plt.axhline(y=max_time, color='y', linestyle='--', label=f"Maxim: {max_time:.2f} ms")

    plt.title(f"Timpul de raspuns pentru {len(response_times)} requesturi (multithread)")
    plt.xlabel("Numar cerere")
    plt.ylabel("Timp de raspuns (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return average_time, min_time, max_time


def measure_POST_response_time(url, data):
    headers = {'Content-Type': 'application/json'}
    start_time = time.perf_counter()
    try:
        response = requests.post(url, json=data, headers=headers)
        end_time = time.perf_counter()

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        return (end_time - start_time) * 1000
    except Exception as e:
        print(f"Request failed: {e}")
        return None


def average_response_time_for_POST(url, data, num_requests):
    response_times = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(measure_POST_response_time, url, data) for _ in range(num_requests)]

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                response_times.append(result)

    if not response_times:
        print("No successful requests.")
        return None, None, None

    average_time = sum(response_times) / len(response_times)
    min_time = min(response_times)
    max_time = max(response_times)

    plt.plot(range(1, len(response_times) + 1), response_times, marker='o', color='b', label="Timp de raspuns (ms)")
    plt.axhline(y=average_time, color='r', linestyle='--', label=f"Media: {average_time:.2f} ms")
    plt.axhline(y=min_time, color='g', linestyle='--', label=f"Minim: {min_time:.2f} ms")
    plt.axhline(y=max_time, color='y', linestyle='--', label=f"Maxim: {max_time:.2f} ms")

    plt.title(f"Timpul de raspuns pentru {len(response_times)} requesturi (multithread)")
    plt.xlabel("Numar cerere")
    plt.ylabel("Timp de raspuns (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return average_time, min_time, max_time
