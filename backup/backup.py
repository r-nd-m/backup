# import queue
# import threading
import datetime
import os
import sqlite3
import subprocess
from collections import Counter

from backup.backup.logger import Logger
from backup.backup.logger import MessageType


class Backup:
    """A backup class"""
    # list of source directories
    source_directory = []
    # list of destination directories
    destination_directory = []
    # list of omit rules
    omit_rules = []
    # database name
    database = 'example.db'
    # attribute prefix
    prefix = 'user.backup.'
    # checksum method of choice
    method = 'sha512sum'
    att_sum = prefix + method
    # modification time attribute name
    att_name = 'st_mtime'
    att_time = prefix + att_name

    # attribute redundancy
    # TODO: more than 1 digit
    # TODO: remove excessive number of attributes
    att_number = 3

    def __init__(self):
        pass

    def backup_start(self):
        connection = sqlite3.connect(Backup.database)
        Logger.init_database(connection)
        session_id = Logger.get_last_session_id(connection)
        Logger.insert_into_log(connection, datetime.datetime.now(), 'I', '101')
        print(session_id)

        # for each entry in source?
        # log ?
        Backup.session_start(connection)
        # post backup?
        connection.close()

    def session_start(self):
        # log session start
        Backup.get_files(self)
        # log on no files?
        Backup.clear_files(self)
        # log on no files?
        Backup.process_files(self)
        # log session end

    def get_files(self):
        """
        :param self:
        :return: Method returns a list of files found in the source path
        """
        pass

    def clear_files(self):
        """
        :param self:
        :return: Method returns a list of files eligible for processing
        """
        pass

    def process_files(self):
        """
        :param self:
        :return:
        """
        # there should be queue wrapper here

        Backup.analyze_file("")
        # for each destination?
        Backup.backup_file("")

    def log(self):
        pass

    def check(self):
        pass

    @staticmethod
    def analyze_file(file):
        pass

    @staticmethod
    def backup_file(file):
        pass

    @staticmethod
    # temp for creating log and parameter tables
    def session_start(connection):

        cursor = connection.cursor()
        # cursor.execute(statement)

    @staticmethod
    def get_file_checksum_calc(file: str):
        # using external checksum commands due to performance considerations
        cmd = [Backup.method, file]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        checksum = out.decode(encoding='utf-8').split(" ")[0]
        return checksum

    @staticmethod
    def get_file_mtime_calc(file: str):
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
    def get_file_atts_calc(file: str):
        return (Backup.get_file_checksum_calc(file),
                Backup.get_file_mtime_calc(file))

    @staticmethod
    def get_file_atts_read(file: str):
        # reading all at once to minimize data access
        xattr_list = os.listxattr(file)
        file_attributes_sum = [None]*Backup.att_number
        file_attributes_time = [None]*Backup.att_number

        for xattr in xattr_list:
            for att in range(Backup.att_number):
                att_sum_cur = Backup.att_sum + '_' + str(att)
                att_time_cur = Backup.att_time + '_' + str(att)

                if xattr == att_sum_cur:
                    raw_attribute = os.getxattr(file, att_sum_cur)
                    file_attributes_sum[att] = \
                        raw_attribute.decode(encoding='utf-8')
                elif xattr == att_time_cur:
                    raw_attribute = os.getxattr(file, att_time_cur)
                    file_attributes_time[att] = \
                        raw_attribute.decode(encoding='utf-8')

        sum_most_common, error_level = \
            Backup.get_most_common_att(file_attributes_sum)
        time_most_common, error_level = \
            Backup.get_most_common_att(file_attributes_time)

        return (sum_most_common, time_most_common, error_level)

    @staticmethod
    def get_most_common_att(att_list: list):

        # default error_level
        error_level = MessageType.success

        att_iter = (att for att in att_list)
        att_count = Counter(att_iter)

        atts_most_common = att_count.most_common(2)

        if atts_most_common.__len__() > 1:
            if (atts_most_common[0][1] == atts_most_common[1][1]) or \
               (atts_most_common[0][1] < Backup.att_number/2):
                error_level = MessageType.error
                most_common_val = ''
            else:
                error_level = MessageType.warning
                most_common_val = atts_most_common[0][0]
        else:
            most_common_val = atts_most_common[0][0]

        return (most_common_val, error_level)

    @staticmethod
    def set_file_atts(file: str, file_atts: list):
        for att in range(Backup.att_number):
            os.setxattr(file,
                        Backup.att_sum + '_' + str(att),
                        bytes(file_atts[0], 'utf-8'))
            os.setxattr(file,
                        Backup.att_time + '_' + str(att),
                        bytes(file_atts[1], 'utf-8'))

    @staticmethod
    def clear_file_atts(file: str, file_atts: list):
        pass

    @staticmethod
    def clear_file_att(file:str, file_att: str):
        pass

    # TODO boundaries
    # TODO sprawdzić kopiowanie atrybutów
    # TODO whole messages instead of errors