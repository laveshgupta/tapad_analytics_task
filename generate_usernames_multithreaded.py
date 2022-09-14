import json
from pathlib import Path
import requests
import threading

key_url = "https://ugener.com/app/identity?locale=en_US&gender=null"
username_url = "https://public-sonjj.p.rapidapi.com/identity?locale=en_US&gender=null&key=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImRhdGFcIjp7XCJsb2NhbGVcIjpcImVuX1VTXCIsXCJnZW5kZXJcIjpcImZlbWFsZVwiLFwibWluQWdlXCI6XCIxOFwiLFwibWF4QWdlXCI6XCI3MFwiLFwiZG9tYWluXCI6XCJ1Z2VuZXIuY29tXCJ9LFwiY3JlYXRlZF9hdFwiOjE2NjMwOTIwODV9Ig.Lo7hFpzMe3W470LyfkxxtgkVoMLMGBuWWzZ1HCwqxTY&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
username_count = 10000
thread_count = 40
num_username_per_thread = int(username_count/thread_count)
username_filename = "usernames.txt"


class UsernameGenerator(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = f"Thread-{self.thread_id}"
        self.usernames = []

    def run(self):
        print(f"Thread: {self.thread_name} Start generating usernames")
        self.usernames = generate_usernames()
        print(f"Thread: {self.thread_name} DONE generating usernames")


def load_usernames():
    usernames = []
    username_filepath = Path(username_filename)
    if username_filepath.exists():
        with open(username_filename) as f:
            usernames = f.read().splitlines()
    return usernames


def save_usernames(usernames):
    # print(f"usernames: {usernames}")
    len_usernames = len(usernames)
    with open(username_filename, 'w') as f:
        for i in range(len_usernames - 1):
            f.write(f"{usernames[i]}\n")
        f.write(usernames[len_usernames-1])


def get_api_key():
    # print("Generating API Key")
    api_key = None
    while not api_key:
        res = requests.get(key_url)
        if res.status_code == 200:
            api_key = json.loads(res.text)['items']
    return api_key


def generate_usernames():
    usernames = []
    current_username_count = 0
    api_key = get_api_key()
    username_url = f"https://public-sonjj.p.rapidapi.com/identity?locale=en_US&gender=null&key={api_key}&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
    while(current_username_count < num_username_per_thread):
        status_code, username = generate_username(username_url)
        if status_code == 200:
            usernames.append(username)
            current_username_count += 1
            if current_username_count % 10 == 0:
                print(
                    f"{threading.current_thread()}    Current Username Count: {current_username_count}    "
                    f"Remaining: {num_username_per_thread-current_username_count}    "
                    f"Username Count Per Thread: {num_username_per_thread}"
                )
            # print(f"current_username_count: {current_username_count}    status_code: {status_code}")
        else:
            api_key = get_api_key()
            username_url = f"https://public-sonjj.p.rapidapi.com/identity?locale=en_US&gender=null&key={api_key}&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
    print(
        f"{threading.current_thread()}    Current Username Count: {current_username_count}    "
        f"Remaining: {num_username_per_thread-current_username_count}    "
        f"Username Count Per Thread: {num_username_per_thread}"
    )
    return usernames


def generate_username(username_url):
    username = None
    res = requests.get(username_url)
    if res.status_code == 200:
        username = json.loads(res.text)['items']['username']
    return res.status_code, username


def main():
    file_usernames = load_usernames()

    username_generator_threads = []
    for i in range(1, thread_count+1):
        username_generator_thread = UsernameGenerator(i)
        username_generator_thread.start()
        username_generator_threads.append(username_generator_thread)

    for username_generator_thread in username_generator_threads:
        username_generator_thread.join()

    for username_generator_thread in username_generator_threads:
        if username_generator_thread.usernames:
            file_usernames.extend(username_generator_thread.usernames)
    file_usernames = list(set(file_usernames))
    save_usernames(file_usernames)


if __name__ == '__main__':
    main()
