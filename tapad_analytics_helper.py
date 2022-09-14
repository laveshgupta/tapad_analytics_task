from flask import request as frequest
from flask import current_app
import json
from datetime import datetime
import redis
import hiredis


class TapadAnalyticsHelper:

    @staticmethod
    def post_analytics(analytics_params):
        timestamp = analytics_params.get('timestamp')
        date_hour = analytics_params.get('date_hour')
        user = analytics_params.get('user')
        click = analytics_params.get('click')
        impression = analytics_params.get('impression')

        users_key = f"{date_hour}:users"
        hash_key = f"{date_hour}"

        redis_client = redis_pool.get_redis_client()
        with redis_client.pipeline() as post_analytics_pipeline:
            retry_count = 0
            while True:
                try:
                    post_analytics_pipeline.watch(users_key, hash_key)
                    user_key_exists = post_analytics_pipeline.exists(users_key)
                    hash_key_exists = post_analytics_pipeline.exists(hash_key)
                    if user_key_exists and hash_key_exists:
                        user_present = post_analytics_pipeline.sismember(users_key, user)
                        post_analytics_pipeline.multi()
                        if click:
                            post_analytics_pipeline.hincrby(hash_key, "clicks", 1)
                        if impression:
                            post_analytics_pipeline.hincrby(hash_key, "impressions", 1)
                        if not user_present:
                            post_analytics_pipeline.hincrby(hash_key, "unique_users", 1)
                            post_analytics_pipeline.sadd(users_key, user)
                        post_analytics_pipeline.execute()
                    else:
                        dict_value = {
                            "unique_users": 1,
                            "clicks": 1 if click else 0,
                            "impressions": 1 if impression else 0,
                        }
                        post_analytics_pipeline.multi()
                        post_analytics_pipeline.sadd(users_key, user)
                        post_analytics_pipeline.hmset(hash_key, dict_value)
                        post_analytics_pipeline.execute()
                    break
                except redis.WatchError:
                    retry_count += 1
                    logger.warning(f"Watcherror on posting analytics. Tried {retry_count} times")
        return TapadAnalyticsHelper.create_response(
            res_body="",
            res_code=200
        )


    @staticmethod
    def get_analytics(analytics_params):
        date_hour = analytics_params.get('date_hour')
        hash_key = f"{date_hour}"
        response_string = ""
        redis_client = redis_pool.get_redis_client()

        if not redis_client.exists(hash_key):
            response_string = "unique_users,0\nclicks,0\nimpressions,0"
        else:
            value = redis_client.hgetall(hash_key)
            response_string = f"unique_users,{value['unique_users']}\nclicks,{value['clicks']}\nimpressions,{value['impressions']}\n"
        return TapadAnalyticsHelper.create_response(
            res_body=response_string,
            res_code=200
        )


    @staticmethod
    def validate_request(request_method):
        """
            Function to validate bid request
        """
        parameters_not_present = []
        request_data = {}
        if frequest.args:
            request_data = frequest.args
        elif frequest.form:
            request_data = frequest.form
        elif frequest.json:
            request_data = frequest.json
        else:
            request_data = json.loads(frequest.data)

        timestamp = request_data.get('timestamp')
        if not timestamp and timestamp != 0:
            parameters_not_present.append('timestamp')
        if request_method == 'POST':
            user = request_data.get('user')
            click = 'click' in request_data
            impression = 'impression' in request_data
            if not user:
                parameters_not_present.append('user')
            if not click and not impression:
                parameters_not_present.extend(['click', 'impression'])

        if parameters_not_present:
            return TapadAnalyticsHelper.create_response(
                res_body=f"Analytics {request_method} Request cannot be processed as these parameters {parameters_not_present} are not passed",
                res_code=400
            )
        else:
            try:
                timestamp = float(timestamp)
                timestamp_secs = datetime.fromtimestamp(timestamp/1000.0)
                date_hour = timestamp_secs.strftime('%Y-%m-%d-%H')
            except Exception as e:
                logger.exception(e)
                return TapadAnalyticsHelper.create_response(
                    res_body=f"Analytics {request_method} due to incorrect timestamp {timestamp}",
                    res_code=400
                )
        r_data = {
            'timestamp': timestamp,
            'date_hour': date_hour,
        }
        if request_method == 'POST':
            r_data['user'] = user
            r_data['click'] = click
            r_data['impression'] = impression
        return r_data


    @staticmethod
    def create_response(res_body: str, res_code: int=200):
        """
        Function to create response for request
        """
        output = res_body
        mime_type = 'text/plain'
        return current_app.response_class(
            response=output,
            status=res_code,
            mimetype=mime_type
        )