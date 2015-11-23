# --*--codding:utf-8--*--

"""Database query wrapper decorator for setting connection and execute queries.
http://ryaneirwin.com/2014/05/31/python-decorators-and-exception-handling/
"""

import ConfigParser
import os

import MySQLdb


class DatabaseWrapperClass(object):

    """Accepts a database connection, creates a cursor,
    and calls the wrapped function, the wrapped function
    has the first argument as a cursor object instead of a connection object.
    """

    def connect_db(self):
        """Reads connection configuration and establishes connection.

        :Return:
            MySQLdb connection.

        :Exceptions:
            - `MySQLdb.Error`: SQL error occurred.
            - `DBError`: Database configuration error.
        """
        try:
            config = ConfigParser.ConfigParser()
            dirname = os.getcwd()
            dbconf = os.path.join(dirname, 'db.conf')
            config.read(dbconf)

            host = config.get(self.conn_name, 'host')
            port = int(config.get(self.conn_name, 'port'))
            user = config.get(self.conn_name, 'user')
            passwd = config.get(self.conn_name, 'password')
            db = config.get(self.conn_name, 'db')

            try:
                conn = MySQLdb.connect(host=host, port=port, user=user,
                                       passwd=passwd, db=db)
            except MySQLdb.Error as err:
                raise UploaderError("SQL error occurred111: %s" % (err,))
        except (ConfigParser.Error, OSError, IOError) as err:
            raise DBError("Database configuration error: %s" % (err,))
        return conn

    def __init__(self, conn_name):
        """Sets connection name, name used to read database configuration
        """
        self.conn_name = conn_name

    def __call__(self, func):
        """Decorates function with MySQL connection establishment and closing.

        :Parameters:
            - `func`: function which requires decoration.

        :Return:
            Function decorated with MySQL connection establishment and
            closing.

        :Exceptions:
            - `DBError`: SQL query error occurred.
        """
        def wrapper(*args, **kwargs):
            conn = self.connect_db()
            cursor = conn.cursor()
            try:
                cursor.execute("BEGIN")
                retval = func(cursor, *args, **kwargs)
                cursor.execute("COMMIT")
                return retval
            except (MySQLdb.Error, Exception) as err:
                cursor.execute("ROLLBACK")
                raise DBError("SQL query error occurred: %s" % (err,))
            finally:
                cursor.close()
                conn.close()
        return wrapper

# uploader_conn = DatabaseWrapperClass('uploader')
#
# @uploader_conn
# def add_data(conn, val):
#     """Inserts new record to db.
#
#     :Parameters:
#         - 'conn': MySQLdb connection cursor.
#         - 'url': URL address to add (string).
#     """
#     query = "INSERT INTO table (column) VALUES ('%s')" % (val,)
#     conn.execute(query)
