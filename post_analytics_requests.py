import requests
import time
import threading
from datetime import datetime
import random
from pathlib import Path


USERNAME_FILENAME = "usernames.txt"
CLICK_OR_IMPRESSION = ['click', 'impression']
URL_PREFIX = "http://localhost:8080/analytics?timestamp="

usernames = []
num_threads = 20
num_requests = 100000
num_requests_per_thread = int(num_requests/num_threads)



def load_usernames():
    global usernames
    username_filepath = Path(USERNAME_FILENAME)
    if username_filepath.exists():
        with open(USERNAME_FILENAME) as f:
            usernames = f.read().splitlines()


class PostAnalyticRequest(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = f"Thread-{self.thread_id}"
        self.analytics_post_urls = []


    def run(self):
        print(f"Thread: {self.thread_name} Start generating urls")
        self.analytics_post_urls = generate_analytics_post_urls()
        print(f"Thread: {self.thread_name} Done generating urls")
        send_post_analytics_requests(self.analytics_post_urls)


def send_post_analytics_requests(analytics_post_urls):
    length_urls = len(analytics_post_urls)
    for i, analytics_post_url in enumerate(analytics_post_urls):
        if i % 10 == 0:
            print(
                f"{threading.current_thread()}    Current Urls Processed: {i}    "
                f"Remaining: {length_urls-i}    "
                f"Urls Count Per Thread: {length_urls}"
            )
        res = requests.post(analytics_post_url)

    print(
        f"{threading.current_thread()}    Current Urls Processed: {i}    "
        f"Remaining: {length_urls-i}    "
        f"Urls Count Per Thread: {length_urls}"
    )

def generate_analytics_post_urls():
    analytics_post_urls = []
    
    num_95_percent = int(.95 * num_requests_per_thread)
    current_time_secs = time.time()
    before_1_hr_time_secs = current_time_secs - (1 * 3600)

    current_time_millisecs = int(current_time_secs * 1000)
    before_1_hr_time_millisecs = int(before_1_hr_time_secs * 1000)

    print(f"before_1_hr_time_millisecs: {before_1_hr_time_millisecs}")
    print(f"current_time_millisecs: {current_time_millisecs}")
    

    for i in range(num_95_percent):
        timestamp = random.randint(before_1_hr_time_millisecs, current_time_millisecs)
        username = random.choice(usernames)
        url_suffix = f"{timestamp}&user={username}&{random.choice(CLICK_OR_IMPRESSION)}"
        analytics_post_url = f"{URL_PREFIX}{url_suffix}"
        analytics_post_urls.append(analytics_post_url)

    before_24_hr_time_secs = current_time_secs - (24 * 3600)
    before_24_hr_time_millisecs = int(before_24_hr_time_secs * 1000)

    for i in range(num_requests_per_thread - num_95_percent):
        timestamp = random.randint(before_24_hr_time_millisecs, before_1_hr_time_millisecs)
        username = random.choice(usernames)
        url_suffix = f"{timestamp}&user={username}&{random.choice(CLICK_OR_IMPRESSION)}"
        analytics_post_url = f"{URL_PREFIX}{url_suffix}"
        analytics_post_urls.append(analytics_post_url)
    return analytics_post_urls

def main():
    load_usernames()

    post_analytics_threads = []
    for i in range(1, num_threads+1):
        post_analytics_thread = PostAnalyticRequest(i)
        post_analytics_thread.start()
        post_analytics_threads.append(post_analytics_thread)

    for post_analytics_thread in post_analytics_threads:
        post_analytics_thread.join()

if __name__ == '__main__':
    main()
