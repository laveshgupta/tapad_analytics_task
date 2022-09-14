A server accepts the following HTTP requests:
```
POST /analytics?timestamp={millis_since_epoch}&user={username}&{click|impression}
```
```
GET /analytics?timestamp={millis_since_epoch}
```

When the `POST` request is made, nothing is returned to the client. We simply side-effect and add the details from the request to our tracking data store.

When the `GET` request is made, we return the following information in plain-text to the client, for the hour of the requested timestamp:
```
unique_users,{number_of_unique_usernames}
clicks,{number_of_clicks}
impressions,{number_of_impressions}
```

The server will receive many more `GET` requests (95%) for the **current hour** than for hours in the past (5%).

Most `POST` requests received by the server will contain a timestamp that matches the current timestamp (95%). However, it is possible for the timestamp in a `POST` request to contain a *historic* timestamp (5%) -- e.g. it is currently the eighth hour of the day, yet the request contains a timestamp for hour six of the day.

Additional servers should be able to be spun up, at any time, without effecting the correctness of our metrics.

The `POST` and `GET` endpoints should be optimized for high throughput and low latency.