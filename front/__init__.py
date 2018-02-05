from redis import Redis
import pymysql

pymysql.install_as_MySQLdb()
rs = Redis(host='127.0.0.1')