import os
import time
import threading
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

REEL_URL = input("🎯 Paste your Instagram Reel URL: ")
NUM_VIEWS = int(input("🎯 How many views you want: "))

MAX_THREADS = 10
PROXY_REFRESH_INTERVAL = 600
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X)...",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B)...",
]

proxies = []

def fetch_proxies():
    global proxies
    try:
        proxy_url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all"
        proxy_list = requests.get(proxy_url).text.splitlines()
        proxies = [proxy.strip() for proxy in proxy_list if proxy]
        print(f"[🔵] Proxies fetched: {len(proxies)}")
    except Exception as e:
        print(f"[🔴] Proxy fetch error: {e}")

def get_random_proxy():
    if not proxies:
        fetch_proxies()
    return random.choice(proxies)

def create_driver(proxy=None, user_agent=None):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if proxy:
        options.add_argument(f'--proxy-server=http://{proxy}')
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    return driver

def watch_reel(view_id):
    try:
        proxy = get_random_proxy()
        user_agent = random.choice(USER_AGENTS)
        driver = create_driver(proxy, user_agent)
        driver.get(REEL_URL)
        print(f"[{view_id}] [+] Viewed with Proxy: {proxy} | UA: {user_agent}")
        time.sleep(random.randint(15, 30))
        driver.quit()
    except WebDriverException as e:
        print(f"[{view_id}] [!] Webdriver crash: {e}. Restarting...")
        os.execv(__file__, ['python'] + sys.argv)
    except Exception as e:
        print(f"[{view_id}] [!] Other Error: {e}")

def refresh_proxies_periodically():
    while True:
        fetch_proxies()
        time.sleep(PROXY_REFRESH_INTERVAL)

def view_manager():
    threads = []
    for i in range(NUM_VIEWS):
        t = threading.Thread(target=watch_reel, args=(i+1,))
        threads.append(t)
        t.start()
        if len(threads) >= MAX_THREADS:
            for t in threads:
                t.join()
            threads = []

if __name__ == "__main__":
    print("⚡ Starting IG Reel Views Farm Bot...")
    proxy_thread = threading.Thread(target=refresh_proxies_periodically, daemon=True)
    proxy_thread.start()
    while True:
        try:
            view_manager()
            print("✅ Batch Completed. Restarting for Stability...")
            time.sleep(random.randint(30, 60))
        except Exception as e:
            print(f"[!] Critical Error: {e}. Restarting...")
            time.sleep(10)
      
