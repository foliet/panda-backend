import pymysql
import redis

pymysql.install_as_MySQLdb()

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
cache = redis.Redis(connection_pool=pool)
