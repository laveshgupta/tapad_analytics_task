import redis
from constants import Constants
import json

class RedisConnectionPool:
    __instance = None

    @staticmethod
    def get_instance():
        """
        Singleton function which is responsible so that only one instance of Redis Connection Pool is present.
        """
        if RedisConnectionPool.__instance == None:
            RedisConnectionPool()
        return RedisConnectionPool.__instance


    def __init__(self):
        if RedisConnectionPool.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.__create_redis_conn_pool()
            RedisConnectionPool.__instance = self


    def __create_redis_conn_pool(self):
        """
        Create redis Connection Pool
        """
        logger.info('Creating Redis Connection Pool.')
        redis_config = config.get('redis', {})
        redis_max_conn = redis_config.get('max_conn', Constants.DEFAULT_REDIS_MAX_CONN)
        redis_host = redis_config.get('host', Constants.DEFAULT_REDIS_HOST)
        redis_port = redis_config.get('port', Constants.DEFAULT_REDIS_PORT)
        redis_database = redis_config.get('database', Constants.DEFAULT_REDIS_DATABASE)
        redis_password = redis_config.get('password', Constants.DEFAULT_REDIS_PASSWORD)
        try:
            self.__redis_conn_pool = redis.ConnectionPool(
                max_connections=redis_max_conn,
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_database,
                decode_responses=True,
            )
            logger.info('Successfully created Redis Connection pool.')
        except Exception as e:
            logger.exception('Error in creating Redis connection pool. Exiting.')
            raise e


    def get_redis_client(self):
        """
        Get a redis client from a Connection Pool
        """
        __redis_client = redis.Redis(
            connection_pool=self.__redis_conn_pool
        )
        return __redis_client
