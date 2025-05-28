import tkinter as tk
import requests
import time
import concurrent.futures

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def send_request(url, request_type="GET", data=None):
    try:
        if request_type == "GET":
            response = requests.get(url)
        elif request_type == "POST":
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False
    


def measure_concurrent_output_rate(url, num_requests, request_type="GET", data=None, max_workers=50):
    start_time = time.perf_counter()
    successful_requests = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request, url, request_type, data) for _ in range(num_requests)]

        for future in concurrent.futures.as_completed(futures):
            if future.result():
                successful_requests += 1

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    output_rate = successful_requests / elapsed_time

    return output_rate, successful_requests, elapsed_time


def incremental_output_rate_test(url, result_text, request_type="GET", data=None, threshold_diff=0.05):
    request_counts = []
    output_rates = []

    num_requests = 100
    prev_rate = None

    while True:
        print(f"Test pentru {num_requests} requesturi...")

        rate, success, elapsed = measure_concurrent_output_rate(
            url, num_requests, request_type, data, max_workers=num_requests
        )

        print(f" - Rata de iesire: {rate:.2f} req/s, {success}/{num_requests} reușite în {elapsed:.2f} sec")
        if success == 0:
            return list(zip([0], [0]))

        result_text.insert(tk.END, f"{num_requests} requesturi => {rate:.2f} req/s\n")
        request_counts.append(num_requests)
        output_rates.append(rate)

        if prev_rate:
            if (rate - prev_rate) < 0:
                print(f"Rata stabilizata (diferenta negativa)")
                break
            diff = abs(rate - prev_rate) / prev_rate
            if diff < threshold_diff:
                print(f"Rata stabilizata (diferenta < {threshold_diff * 100:.1f}%)\n")
                break

        prev_rate = rate
        num_requests *= 2

    
    plt.switch_backend('agg')
    plt.figure()
    plt.plot(request_counts, output_rates, marker='o', linestyle='-')
    plt.title("Evoluția ratei de ieșire în funcție de numărul de requesturi")
    plt.xlabel("Număr requesturi")
    plt.ylabel("Rată de ieșire (requesturi/secundă)")
    plt.grid(True)
    plt.savefig("current_grafic.png")
    plt.close()

    return list(zip(request_counts, output_rates))


# def display_concurrent_output_rate(url, num_requests, request_type="GET", data=None, max_workers=50):
#     output_rate, successful_requests, elapsed_time = measure_concurrent_output_rate(
#         url, num_requests, request_type, data, max_workers
#     )
    
#     print(f"Numar total cereri trimise: {num_requests}")
#     print(f"Numar cereri procesate cu succes: {successful_requests}")
#     print(f"Timp total: {elapsed_time:.2f} secunde")
#     print(f"Rata de iesire: {output_rate:.2f} cereri pe secunda")



# def incremental_output_rate_test(url, request_type="GET", data=None, max_workers=50, threshold_diff=0.05):
#     request_counts = []
#     output_rates = []

#     num_requests = 100
#     prev_rate = None

#     while True:
#         print(f"Test pentru {num_requests} requesturi...")
#         rate, success, elapsed = measure_concurrent_output_rate(url, num_requests, request_type, data, max_workers)

#         print(f" - Rata de ieșire: {rate:.2f} req/s, {success}/{num_requests} reușite în {elapsed:.2f} sec")

#         request_counts.append(num_requests)
#         output_rates.append(rate)

#         if prev_rate:
#             diff = abs(rate - prev_rate) / prev_rate
#             if diff < threshold_diff:
#                 print(f"Rata stabilizată (diferență < {threshold_diff * 100:.1f}%)\n")
#                 break
#         prev_rate = rate
#         num_requests *= 2  # dublăm la fiecare pas

#     # Grafic
#     plt.figure()
#     plt.plot(request_counts, output_rates, marker='o', linestyle='-')
#     plt.title("Evoluția ratei de ieșire în funcție de numărul de requesturi")
#     plt.xlabel("Număr requesturi")
#     plt.ylabel("Rată de ieșire (requesturi/secundă)")
#     plt.grid(True)
#     plt.show()

#     return list(zip(request_counts, output_rates))
