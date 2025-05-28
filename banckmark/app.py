import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from response_time_multi_threading import average_response_time_for_GET, average_response_time_for_POST
from output_rate import incremental_output_rate_test

def run_test():
    url = url_entry.get()
    method = method_combo.get()
    test_type = test_type_combo.get()

    try:
        if test_type == "Rată de ieșire":
            num_requests = None
        else:
            num_requests = int(requests_entry.get())
            if num_requests <= 0:
                raise ValueError
    except ValueError:
        messagebox.showerror("Eroare", "Numărul de cereri trebuie să fie un număr pozitiv.")
        return

    # Citim payload dacă e POST
    if method == "POST":
        try:
            data = json.loads(payload_text.get("1.0", tk.END).strip())
        except json.JSONDecodeError:
            messagebox.showerror("Eroare", "JSON invalid.")
            return
    else:
        data = None

    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)

    if test_type == "Timp de răspuns":
        if method == "POST":
            avg, min_, max_ = average_response_time_for_POST(url, data, num_requests)
        else:
            avg, min_, max_ = average_response_time_for_GET(url, num_requests)

        if avg is not None:
            result_text.insert(tk.END, f"Timp mediu: {avg:.2f} ms\n")
            result_text.insert(tk.END, f"Timp minim: {min_:.2f} ms\n")
            result_text.insert(tk.END, f"Timp maxim: {max_:.2f} ms\n")

    elif test_type == "Rată de ieșire":
        results = incremental_output_rate_test(url, method, data)
        for count, rate in results:
            result_text.insert(tk.END, f"{count} requesturi => {rate:.2f} req/s\n")

    result_text.config(state='disabled')

def toggle_request_input(*args):
    if test_type_combo.get() == "Rată de ieșire":
        requests_entry.config(state='disabled')
    else:
        requests_entry.config(state='normal')


# GUI 
root = tk.Tk()
root.title("Testare Performanță Server")


tk.Label(root, text="URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)


tk.Label(root, text="Tip test:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
test_type_combo = ttk.Combobox(root, values=["Timp de răspuns", "Rată de ieșire"], state="readonly")
test_type_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)
test_type_combo.current(0)
test_type_combo.bind("<<ComboboxSelected>>", toggle_request_input)


tk.Label(root, text="Metodă:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
method_combo = ttk.Combobox(root, values=["GET", "POST"], state="readonly")
method_combo.grid(row=2, column=1, sticky="w", padx=5)
method_combo.current(0)
method_combo.bind("<<ComboboxSelected>>", toggle_request_input)


requests_label = tk.Label(root, text="Număr requesturi:")
requests_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
requests_entry = tk.Entry(root)
requests_entry.insert(0, "10")
requests_entry.grid(row=3, column=1, padx=5, pady=5)


payload_label = tk.Label(root, text="Date JSON (POST):")
payload_label.grid(row=4, column=0, sticky="ne")
payload_text = scrolledtext.ScrolledText(root, height=5, width=40)
payload_text.grid(row=4, column=1, padx=5)


run_button = tk.Button(root, text="Rulare test", command=run_test)
run_button.grid(row=5, column=0, columnspan=2, pady=10)


result_text = scrolledtext.ScrolledText(root, height=10, width=60, state='disabled')
result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5)


root.mainloop()
