import response_time
import response_time_multi_threading


url = "http://localhost:8080/"
data = {
    "nume": "Marius"
}



# print (response_time_multi_threading.average_response_time_for_POST(url, data, 100))


import output_rate

url = "http://localhost:8080/"
data = {
    "nume": "Marius"
}

output_rate.incremental_output_rate_test(url, "GET")
