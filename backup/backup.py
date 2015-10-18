# import queue
# import threading
import subprocess
import sqlite3
import os


class Backup:
    """A backup class"""
    # list of source directories
    source_directory = []
    # list of destination directories
    destination_directory = []
    # list of omit rules
    omit_rules = []

    # determine whether we are using root or regular user account
    if os.getlogin() == 'root':
        prefix = 'system'
    else:
        prefix = 'user'

    # checksum method of choice
    method = 'sha512sum'
    # modification time attribute name
    att_name = 'st_mtime'
    att_sum = prefix + '.' + method
    att_time = prefix + '.' + att_name

    def __init__(self):
        pass

    def backup_start(self):
        pass

    def create_database_log1(self):
        pass

    def create_database_log2(self):
        pass

    def get_files(self):
        pass

    def log(self):
        pass

    def check(self):
        pass

    @staticmethod
    def analyze_file(file):
        pass

    @staticmethod
    def log_table_create(connection, table_name):

        t_session = '''CREATE TABLE session
                       ( session_id INTEGER PRIMARY KEY,
                         status CHAR(1) NOT NULL,
                         message CHAR(3) NOT NULL,
                         time_started DATETIME NOT NULL,
                         time_completed DATETIME
                       );'''

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
                    );'''

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
                    );'''

        t_parameter = ''' CREATE TABLE parameter
                    ( session_id INTEGER NOT NULL,
                      parameter_id INTEGER NOT NULL,
                      parameter_name VARCHAR(128) NOT NULL,
                      parameter_value VARCHAR(1024) NOT NULL,
                      PRIMARY KEY (session_id, parameter_id)
                    );'''

        cursor = connection.cursor()

        if table_name == 'Session':
            try:
                cursor.execute(t_session)
            except sqlite3.OperationalError:
                print("Ta tabela już istnieje.")
        elif table_name == 'File':
            cursor.execute(t_file)
        elif table_name == 'Iteration':
            cursor.execute(t_iteration)
        elif table_name == 'Parameter':
            cursor.execute(t_parameter)

    @staticmethod
    def get_file_checksum(file):
        # using external checksum commands due to performance considerations
        cmd = [Backup.method, file]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        checksum = out.decode(encoding='utf-8').split(" ")[0]
        return checksum

    @staticmethod
    def get_file_mtime(file):
        # using external mtime command due to issues with Python's float
        # accuracy and lack of proper timezone formatting
        cmd = ['stat', '--format=%y', file]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        mtime = out.decode(encoding='utf-8').split("\n")[0]
        return mtime

    @staticmethod
    def get_file_attributes_calc(file):
        file_attributes = [None]*2
        file_attributes[0] = Backup.get_file_checksum(file)
        file_attributes[1] = Backup.get_file_mtime(file)
        return file_attributes

    @staticmethod
    def get_file_attributes_read(file):
        xattr_list = os.listxattr(file)
        file_attributes = [None]*2
        for xattr in xattr_list:
            if xattr == Backup.att_sum:
                raw_attribute = os.getxattr(file, Backup.att_sum)
                file_attributes[0] = raw_attribute.decode(encoding='utf-8')
            elif xattr == Backup.att_time:
                raw_attribute = os.getxattr(file, Backup.att_time)
                file_attributes[1] = raw_attribute.decode(encoding='utf-8')
        return file_attributes

    @staticmethod
    def set_file_attributes(file, file_attributes):
        os.setxattr(file, Backup.att_sum, bytes(file_attributes[0], 'utf-8'))
        os.setxattr(file, Backup.att_time, bytes(file_attributes[1], 'utf-8'))
