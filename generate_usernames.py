import json
from pathlib import Path
import requests

key_url = "https://ugener.com/app/identity?locale=en_US&gender=null"
username_url = "https://public-sonjj.p.rapidapi.com/identity?locale=en_US&gender=null&key=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImRhdGFcIjp7XCJsb2NhbGVcIjpcImVuX1VTXCIsXCJnZW5kZXJcIjpcImZlbWFsZVwiLFwibWluQWdlXCI6XCIxOFwiLFwibWF4QWdlXCI6XCI3MFwiLFwiZG9tYWluXCI6XCJ1Z2VuZXIuY29tXCJ9LFwiY3JlYXRlZF9hdFwiOjE2NjMwOTIwODV9Ig.Lo7hFpzMe3W470LyfkxxtgkVoMLMGBuWWzZ1HCwqxTY&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
username_count = 1000
username_filename = "usernames.txt"


def load_usernames():
    usernames = []
    username_filepath = Path(username_filename)
    if username_filepath.exists():
        with open(username_filename) as f:
            usernames = f.read().splitlines()
    return usernames


def save_usernames(usernames):
    print(f"usernames: {usernames}")
    len_usernames = len(usernames)
    with open(username_filename, 'w') as f:
        for i in range(len_usernames - 1):
            f.write(f"{usernames[i]}\n")
        f.write(usernames[len_usernames-1])


def get_api_key():
    print("Generating API Key")
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
    while(current_username_count < username_count):
        status_code, username = generate_username(username_url)
        if status_code == 200:
            usernames.append(username)
            current_username_count += 1
            print(f"current_username_count: {current_username_count}    status_code: {status_code}")
        else:
            api_key = get_api_key()
            username_url = f"https://public-sonjj.p.rapidapi.com/identity?locale=en_US&gender=null&key={api_key}&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
    return usernames


def generate_username(username_url):
    username = None
    res = requests.get(username_url)
    if res.status_code == 200:
        username = json.loads(res.text)['items']['username']
    return res.status_code, username


def main():
    file_usernames = load_usernames()
    # print(f"file_usernames: {file_usernames}")
    for i in range(1):
        usernames = generate_usernames()
        # print(f"usernames: {usernames}")
        if usernames:
            file_usernames.extend(usernames)
            # print(f"file_usernames: {file_usernames}")
    file_usernames = list(set(file_usernames))
    save_usernames(file_usernames)


if __name__ == '__main__':
    main()
