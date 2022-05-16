import pymysql
import redis

pymysql.install_as_MySQLdb()

pool = redis.ConnectionPool(host='1.117.107.95', port=6379, password='fqh66545896.')
cache = redis.Redis(connection_pool=pool)
