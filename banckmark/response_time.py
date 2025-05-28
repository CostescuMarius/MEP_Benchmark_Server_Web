import requests
import time
import sys
import matplotlib.pyplot as plt
    
def measure_GET_response_time(url):
    start_time = time.perf_counter()
    response = requests.get(url)
    end_time = time.perf_counter()
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        sys.exit(1)

    response_time = (end_time - start_time) * 1000

    return response_time


def average_response_time_for_GET(url, num_requests):
    total_time = 0
    min_time = float('inf')
    max_time = 0
    response_times = []  

    for i in range(num_requests):
        print(f"Request {i + 1}/{num_requests}", end='\r')

        response_time = measure_GET_response_time(url)
        response_times.append(response_time)
        total_time += response_time

        if response_time < min_time:
            min_time = response_time
        if response_time > max_time:
            max_time = response_time


    average_time = total_time / num_requests
    
    plt.plot(range(1, num_requests + 1), response_times, marker='o', color='b', label="Timp de raspuns (ms)")
    plt.axhline(y=average_time, color='r', linestyle='--', label=f"Media: {average_time:.2f} ms")
    plt.axhline(y=min_time, color='g', linestyle='--', label=f"Minim: {min_time:.2f} ms")
    plt.axhline(y=max_time, color='y', linestyle='--', label=f"Maxim: {max_time:.2f} ms")
    
    plt.title(f"Timpul de raspuns pentru {num_requests} requesturi")
    plt.xlabel("Numar cerere")
    plt.ylabel("Timp de raspuns (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()
    

    return average_time, min_time, max_time



def measure_POST_response_time(url, data):
    headers = {'Content-Type': 'application/json'}

    start_time = time.perf_counter()
    response = requests.post(url, json=data, headers=headers) 
    end_time = time.perf_counter()

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.reason}")
        sys.exit(1)

    response_time = (end_time - start_time) * 1000

    return response_time


def average_response_time_for_POST(url, data, num_requests):
    total_time = 0
    min_time = float('inf')
    max_time = 0
    response_times = []  

    for i in range(num_requests):
        print(f"Request {i + 1}/{num_requests}", end='\r')

        response_time = measure_POST_response_time(url, data)
        response_times.append(response_time)
        total_time += response_time

        if response_time < min_time:
            min_time = response_time
        if response_time > max_time:
            max_time = response_time


    average_time = total_time / num_requests
    
    plt.plot(range(1, num_requests + 1), response_times, marker='o', color='b', label="Timp de raspuns (ms)")
    plt.axhline(y=average_time, color='r', linestyle='--', label=f"Media: {average_time:.2f} ms")
    plt.axhline(y=min_time, color='g', linestyle='--', label=f"Minim: {min_time:.2f} ms")
    plt.axhline(y=max_time, color='y', linestyle='--', label=f"Maxim: {max_time:.2f} ms")
    
    plt.title(f"Timpul de raspuns pentru {num_requests} requesturi")
    plt.xlabel("Numar cerere")
    plt.ylabel("Timp de raspuns (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()
    

    return average_time, min_time, max_time
