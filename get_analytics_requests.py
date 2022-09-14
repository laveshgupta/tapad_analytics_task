import requests
import time
import threading
from datetime import datetime
import random
from pathlib import Path

URL_PREFIX = "http://localhost:8080/analytics?timestamp="
num_threads = 10
num_requests = 1000
num_requests_per_thread = int(num_requests/num_threads)

class GetAnalyticRequest(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = f"Thread-{self.thread_id}"
        self.analytics_post_urls = []


    def run(self):
        print(f"Thread: {self.thread_name} Start generating urls")
        self.analytics_post_urls = generate_analytics_get_urls()
        print(f"Thread: {self.thread_name} Done generating urls")
        send_get_analytics_requests(self.analytics_post_urls)


def send_get_analytics_requests(analytics_post_urls):
    length_urls = len(analytics_post_urls)
    for i, analytics_post_url in enumerate(analytics_post_urls):
        timestamp = int(analytics_post_url[len(URL_PREFIX):])
        res = requests.get(analytics_post_url)
        print(
            f"{threading.current_thread()}    Current Urls Processed: {i}    "
            f"Remaining: {length_urls-i}    "
            f"Urls Count Per Thread: {length_urls}    "
            f"TIMESTAMP: {timestamp}    "
            f"DATEHOUR: {datetime.fromtimestamp(timestamp/1000.0).strftime('%Y-%m-%d-%H')}    "
            f"OUTPUT: {res.text}"
        )


def generate_analytics_get_urls():
    analytics_get_urls = []
    
    num_95_percent = int(.95 * num_requests_per_thread)
    current_time_secs = time.time()
    before_1_hr_time_secs = current_time_secs - (1 * 3600)

    current_time_millisecs = int(current_time_secs * 1000)
    before_1_hr_time_millisecs = int(before_1_hr_time_secs * 1000)

    for i in range(num_95_percent):
        timestamp = random.randint(before_1_hr_time_millisecs, current_time_millisecs)
        url_suffix = f"{timestamp}"
        analytics_post_url = f"{URL_PREFIX}{url_suffix}"
        analytics_get_urls.append(analytics_post_url)

    before_24_hr_time_secs = current_time_secs - (24 * 3600)
    before_24_hr_time_millisecs = int(before_24_hr_time_secs * 1000)

    for i in range(num_requests_per_thread - num_95_percent):
        timestamp = random.randint(before_24_hr_time_millisecs, before_1_hr_time_millisecs)
        url_suffix = f"{timestamp}"
        analytics_post_url = f"{URL_PREFIX}{url_suffix}"
        analytics_get_urls.append(analytics_post_url)
    return analytics_get_urls

def main():
    get_analytics_threads = []
    for i in range(1, num_threads+1):
        get_analytics_thread = GetAnalyticRequest(i)
        get_analytics_thread.start()
        get_analytics_threads.append(get_analytics_thread)

    for get_analytics_thread in get_analytics_threads:
        get_analytics_thread.join()

if __name__ == '__main__':
    main()