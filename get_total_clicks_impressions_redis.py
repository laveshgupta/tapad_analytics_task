import redis


def get_redis_client():
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, password="ORQXAYLE", decode_responses=True,)
    return redis_client

def get_all_redis_keys():
    redis_client = get_redis_client()
    redis_keys = redis_client.keys()
    return redis_keys


def get_hash_redis_keys(redis_keys):
    hash_keys = []
    for redis_key in redis_keys:
        if 'users' not in redis_key:
            hash_keys.append(redis_key)
    return hash_keys


def print_stats(hash_keys):
    redis_client = get_redis_client()
    total_usernames = total_clicks = total_impressions = 0
    sorted_hash_keys = sorted(hash_keys)
    print(f"SORT: {sorted_hash_keys}")
    for hash_key in sorted_hash_keys:
        value = redis_client.hgetall(hash_key)
        unique_users = int(value['unique_users'])
        clicks = int(value['clicks'])
        impressions = int(value['impressions'])
        total_usernames += unique_users
        total_clicks += clicks
        total_impressions += impressions
        print(
            f"DATEHOUR: {hash_key}    UNIQUE USERS: {unique_users}    CLICKS: {clicks}    IMPRESSIONS: {impressions}    "
            f"TOTAL USERNAMES: {total_usernames}    TOTAL CLICKS: {total_clicks}    TOTAL IMPRESSIONS: {total_impressions}"
        )
    print(f"TOTAL CLICKS AND IMPRESSIONS: {total_clicks + total_impressions}")


def main():
    redis_keys = get_all_redis_keys()
    hash_keys = get_hash_redis_keys(redis_keys)
    print_stats(hash_keys)


if __name__ == '__main__':
    main()