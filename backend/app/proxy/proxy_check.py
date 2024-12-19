import threading
import queue
import requests

queue = queue.Queue()
valid_proxies = []

with open("C:/Users/drfis/Codes/IA_Instagram/backend/app/proxy/proxy_list.txt", "r") as file:
    proxies = file.read().splitlines()
    for p in proxies:
        queue.put(p)

def check_proxies():
    while not queue.empty():
        proxy = queue.get()
        try:
            res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=2)
        except:
            continue
        if res.status_code == 200:
            print(proxy)

for _ in range(10):
    threading.Thread(target=check_proxies).start()