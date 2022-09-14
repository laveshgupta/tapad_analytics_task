from logger import Logger
from redis_connection_pool import RedisConnectionPool
from config import Config
from constants import Constants
from flask import Flask, request, Response
from tapad_analytics_helper import TapadAnalyticsHelper as tah


class TapadAnalyticsServer:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.create_routes()


    def server_run(self):
        """
        Starting flask server
        """
        flask_config = config.get('flask', {})
        flask_host = flask_config.get('host', Constants.APP_HOST)
        flask_port = flask_config.get('port', Constants.APP_PORT)
        self.app.run(
            host=flask_host,
            port=flask_port,
            debug=True
        )


    def create_routes(self):
        """
        Create routes in application
        """
        #Route to serve campaign requests
        @self.app.route('/analytics', methods=['POST', 'GET'])
        def get_or_save_analytics():
            request_method = request.method
            analytics_params = tah.validate_request(request_method)
            if isinstance(analytics_params, Response):
                return analytics_params

            if request_method == 'POST':
                res = tah.post_analytics(analytics_params)
            elif request_method == 'GET':
                res = tah.get_analytics(analytics_params)

            return res


if __name__ == '__main__':
    config = Config()
    __builtins__.config = config
    logger = Logger()
    __builtins__.logger = logger
    redis_pool = RedisConnectionPool()
    __builtins__.redis_pool = redis_pool
    kbts = TapadAnalyticsServer()
    kbts.server_run()