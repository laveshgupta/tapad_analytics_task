# Tapad Analytics
This repo is created to solve Task Assignment to create a analytics server

## File Structure
* config.py:- This is used to have config for the application
* constants.py:- This file contains all the constants value
* docker-compose.yml:- This file is used to start all the services such as nginx, analyticsserver and redis.
* dockerfile:- This file creates the docker image for analyticsserver. It will be used for docker-compose for running infra.
* generate_usernames_multithreaded.py:- This file uses multithreading to get usernames from online link. It is saved in usernames.txt and will be used by post_analytics_requests.py for posting request.
* generate_usernames.py:- This file gets usernames from online link. It is saved in usernames.txt and will be used by post_analytics_requests.py for posting request.
* get_analytics_requests.py:- This file emulates get part of analytics requests.
* get_total_clicks_impressions_redis.py:- This file gets usernames, clicks and impressions pertaining to datehour from Redis. Used to tally total clicks+impressions with number of requests.
* logger.py:- This file defined logger for logging messages.
* nginx.conf:- This creates the configuration for nginx to serves requests for analytics server.
* post_analytics_requests.py:- This file emulates post part of analytics requests. It post analytics requests based on the criteria, that 95% of the requests will be of latest hour timestamp and 5% can be old
* redis_connection_pool.py:- This file is used to create Redis connection pool and to give Redis client from Redis connection pool.
* requirements.txt:- This file specifies all the packages to run above application. Run this as `pip3 install -r requirements.txt`
* tapad_analytics_helper.py:- This file consists of helper functions to serve api requests.
* tapad_analytics_server.py:- Run this file to start the server and the apis. Executing this is through docker-compose, but if you want to run standalone, install dependencies mentioned in requirements.txt using python 3.9.14. Command to run ```python3 tapad_analytics_server.py```.
* tapad_analytics_task.json:- This json file can be used to alter default values specified in constants.py file




# APIs created
Created two APIs. One for the posting analytics and second one to get analytics

* Post Analytics API: POST /analytics
```
REQUEST: POST /analytics?timestamp={millis_since_epoch}&user={username}&{click|impression}
RESPONSE: HTTP/1.1 200 Created
```

* Get Analytics API: GET /analytics
```
REQUEST: GET /analytics?timestamp={millis_since_epoch}
RESPONSE: HTTP/1.1 200 Created
            unique_users,{number_of_unique_usernames}
            clicks,{number_of_clicks}
            impressions,{number_of_impressions}
```

# Run Application

 Install docker-compose on system. 

 To start a single analyticsserver, run

 ```
 docker-compose up --build -d
 ```

 To stop all services:- analyticsserver, redis and nginx, run

 ```
 docker-compose down
 ```

 To start multiple analyticsservers, run

 ```
 docker-compose up --build --scale analyticsserver=<num_server> -d
 docker-compose up --build --scale analyticsserver=4 -d
 ```