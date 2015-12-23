import datetime
import sqlite3


class Message:
    """A message class"""

    log_table_created_log = ['I','001']
    log_table_created_session = ['I', '002']
    log_table_created_file = ['I', '003']
    log_table_created_iteration = ['I', '004']
    log_table_created_parameter = ['I', '005']

class Logger:
    """A logger class"""

    @staticmethod
    def init_database(connection):
        Logger.__table_create(connection, 'Log')
        Logger.__table_create(connection, 'Session')
        Logger.__table_create(connection, 'File')
        Logger.__table_create(connection, 'Iteration')
        Logger.__table_create(connection, 'Parameter')

    @staticmethod
    def __insert_into_table(connection, table_name, values):
        """Insert into table"""
        cursor = connection.cursor()

        t_log = '''INSERT INTO log (timestamp,
                                    status,
                                    message)
                   VALUES (?, ?, ?)'''

        t_session = '''INSERT INTO session (session_id,
                                            status,
                                            message,
                                            time_started,
                                            time_completed)
                       VALUES (?, ?, ?, ?, ?)'''

        t_file = '''INSERT INTO file (session_id,
                                      file_id,
                                      status,
                                      message,
                                      time_started,
                                      time_completed,
                                      directory,
                                      file,
                                      sha512sum_old,
                                      mtime_old,
                                      sum512sum_new,
                                      mtime_new)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        t_iteration = '''INSERT INTO iteration (session_id,
                                                file_id,
                                                iteration_id,
                                                status,
                                                message,
                                                time_started,
                                                time_completed,
                                                directory_source,
                                                file_source,
                                                directory_destination,
                                                file_destination)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        t_parameter = '''INSERT INTO parameter (session_id
                                                parameter_id
                                                parameter_name
                                                parameter_value)
                         VALUES (?, ?, ?, ?)'''

        if table_name == 'Log':
            statement = t_log
        elif table_name == 'Session':
            statement = t_session
        elif table_name == 'File':
            statement = t_file
        elif table_name == 'Iteration':
            statement = t_iteration
        elif table_name == 'Parameter':
            statement = t_parameter
        else:
            statement = None

        try:
            cursor.execute(statement, values)
            connection.commit()
        except ValueError:
            print("ValueError")
        except TypeError:
            print("TypeError")


    @staticmethod
    def insert_into_log(connection, timestamp, status, message):
        """
        This method insert one line into the Log table
        :param connection: a database connection
        :param timestamp: current (local) timestamp
        :param status:
        :param message:
        :return:
        """

        try:
            Logger.__insert_into_table(connection,
                                      'Log',
                                      (timestamp, status, message))
        except sqlite3.OperationalError:
            print("OperationalError")


    @staticmethod
    def update_table(connection, table_name, values):
        """Update table"""
        cursor = connection.cursor()

        t_session = '''UPDATE session
                          SET status = ?,
                              message = ?,
                              time_started = ?,
                              time_completed = ?
                        WHERE session_id = ?'''

        t_file = '''UPDATE file
                       SET status = ?,
                           message = ?,
                           time_started = ?,
                           time_completed = ?,
                           directory = ?,
                           file = ?,
                           sha512sum_old = ?,
                           mtime_old = ?,
                           sum512sum_new = ?,
                           mtime_new = ?
                     WHERE session_id = ? AND
                           file_id = ?'''

        t_iteration = '''UPDATE iteration
                            SET status = ?,
                                message = ?,
                                time_started = ?,
                                time_completed = ?,
                                directory_source = ?,
                                file_source = ?,
                                directory_destination = ?,
                                file_destination = ?
                          WHERE session_id = ? AND
                                file_id = ? AND
                                iteration_id = ?'''

        if table_name == 'Session':
            statement = t_session
        elif table_name == 'File':
            statement = t_file
        elif table_name == 'Iteration':
            statement = t_iteration
        else:
            statement = None

        try:
            cursor.execute(statement, *values)
        except ValueError:
            print("This should have never happened")

    @staticmethod
    def get_last_session_id(connection):
        cursor = connection.cursor()

        tables = ['session', 'file', 'iteration', 'parameter']
        max_id = 0

        for table in tables:
            cursor.execute('SELECT MAX(session_id) as last_id FROM ' + table)
            max_table_id = cursor.fetchone()[0]

            try:
                if max_table_id > max_id:
                    max_id = max_table_id

            except TypeError:
                # nothing to do here
                pass

        return max_id

    @staticmethod
    def __table_create(connection, table_name):

        t_log = '''CREATE TABLE log
                ( timestamp DATETIME NOT NULL,
                  status CHAR(1) NOT NULL,
                  message CHAR(3) NOT NULL
                )'''

        t_session = '''CREATE TABLE session
                       ( session_id INTEGER PRIMARY KEY,
                         status CHAR(1) NOT NULL,
                         message CHAR(3) NOT NULL,
                         time_started DATETIME NOT NULL,
                         time_completed DATETIME
                       )'''

        t_file = '''CREATE TABLE file
                    ( session_id INTEGER NOT NULL,
                      file_id INTEGER NOT NULL,
                      status CHAR(1) NOT NULL,
                      message CHAR(3) NOT NULL,
                      time_started DATETIME NOT NULL,
                      time_completed DATETIME,
                      directory VARCHAR(1024) NOT NULL,
                      file VARCHAR(255) NOT NULL,
                      sha512sum_old CHAR(128),
                      mtime_old CHAR(35),
                      sum512sum_new CHAR(128) NOT NULL,
                      mtime_new CHAR(35) NOT NULL,
                      PRIMARY KEY (session_id, file_id)
                    )'''

        t_iteration = ''' CREATE TABLE iteration
                    ( session_id INTEGER NOT NULL,
                      file_id INTEGER NOT NULL,
                      iteration_id INTEGER NOT NULL,
                      status CHAR(1) NOT NULL,
                      message CHAR(3) NOT NULL,
                      time_started DATETIME NOT NULL,
                      time_completed DATETIME,
                      directory_source VARCHAR(1024) NOT NULL,
                      file_source VARCHAR(255) NOT NULL,
                      directory_destination VARCHAR(1024) NOT NULL,
                      file_destination VARCHAR(255) NOT NULL,
                      PRIMARY KEY (session_id, file_id, iteration_id)
                    )'''

        t_parameter = ''' CREATE TABLE parameter
                    ( session_id INTEGER NOT NULL,
                      parameter_id INTEGER NOT NULL,
                      parameter_name VARCHAR(128) NOT NULL,
                      parameter_value VARCHAR(1024) NOT NULL,
                      PRIMARY KEY (session_id, parameter_id)
                    )'''

        if table_name == 'Log':
            statement = t_log
        elif table_name == 'Session':
            statement = t_session
        elif table_name == 'File':
            statement = t_file
        elif table_name == 'Iteration':
            statement = t_iteration
        elif table_name == 'Parameter':
            statement = t_parameter
        else:
            statement = None

        cursor = connection.cursor()

        try:
            cursor.execute(statement)
            Logger.insert_into_log(connection, datetime.datetime.now(), 'I', '')
        except sqlite3.OperationalError:
            print("OperationalError")

