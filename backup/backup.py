# import queue
# import threading
import configparser
import datetime
import os
import re
import sqlite3
import subprocess
import string
from collections import Counter
from collections import namedtuple
from distutils.command.config import config

from backup.backup.logger import Logger
from backup.backup.logger import MessageType


class Backup:
    """A backup class"""

    config_file = './../backup/config.ini'

    # attribute redundancy
    # TODO: more than 1 digit
    # TODO: remove excessive number of attributes

    # required for named tuples
    global_config = 0
    sessions_config = 1

    att_number = 3
    valid_sum_atts = []
    valid_time_atts = []
    method = 'sha512sum'
    att_name = 'st_mtime'
    att_sum =  'user.backup.sha512sum'
    att_time = 'user.backup.st_mtime'

    def __init__(self):
        self.config = self.parse_config(self.config_file)
        print(self.config)

    def parse_config(self, config_file: str):
        # extended interpolation for complex variables
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

        config.read(config_file)

        # first part of the config file is a Global section
        GlobalConfig = namedtuple('GlobalConfig', config.options(config.sections()[0]))
        global_config = GlobalConfig(*config[config.sections()[0]].values())

        # second and further sections of the config file are Sessions sections
        SessionConfig = namedtuple('SessionConfig', config.options(config.sections()[1]))
        sessions = [session for session in config.sections() if str(session).split('_')[0] == 'SESSION']
        sessions_values = [config[session].values() for session in sessions]
        session_config = [SessionConfig(*value) for value in sessions_values]

        # return a config tuple
        return (global_config, session_config)

    def backup_start(self):
        # connection = sqlite3.connect(self.config[self.global_config].database)

        for session_config in self.config[self.sessions_config]:
            self.session_start(session_config)

        # Logger.init_database(connection)
        # session_id = Logger.get_last_session_id(connection)
        # Logger.insert_into_log(connection, datetime.datetime.now(), 'I', '101')
        # print(session_id)

        # for each entry in source?
        # log ?
        # Backup.session_start(connection)
        # post backup?
        # connection.close()

    def session_start(self, session: namedtuple):
        for source_directory in session.source_directory.split(' '):
            for root, dirs, files in os.walk(source_directory, topdown=True):
                omit_rules = session.omit_rules.split(' ')
                (files, dirs) = self.get_filtered_file_list(files, dirs, omit_rules)

                os.chdir(root)
                for file in files:
                    self.process_file(root, file)

        # log session start
        #Backup.get_files(self)
        # log on no files?
        #Backup.clear_files(self)
        # log on no files?
        #Backup.process_files(self)
        # log session end

    def get_filtered_file_list(self, files: list, dirs: list, omit_rules: list):
        """
        :param self:
        :return: Method returns a list of directories and files
        :eligible for processing
        """

        for rule in omit_rules:
            regex = re.compile(rule)
            filtered_files = [f for f in files if not regex.search(f)]
            filtered_dirs = [d for d in dirs if not regex.search(d)]

        return (filtered_files, filtered_dirs)

    def get_removed_file_lists(self, files: list, dirs: list, omit_rules: list):
        """
        :param self:
        :return: Method returns a list of directories and files *not*
        :eligible for processing (for testing purposes)
        """

        for rule in omit_rules:
            regex = re.compile(rule)
            deleted_files = [f for f in files if regex.search(f)]
            deleted_dirs = [d for d in dirs if regex.search(d)]

        return (deleted_files, deleted_dirs)

    def process_file(self, root: string, file: list):
        """
        :param self:
        :return:
        """
        # there should be queue wrapper here

        print(root, file)
        self.analyze_file(file)

        #Backup.analyze_file("")
        # for each destination?
        # Backup.backup_file("")

    def log(self):
        pass

    def check(self):
        pass

    @staticmethod
    def analyze_file(file):
        file_attributes_calc = Backup.get_file_atts_calc(file)
        file_attributes_read = Backup.get_file_atts_read(file)[0:2]
        print(file_attributes_calc)
        print(file_attributes_read)

    @staticmethod
    def backup_file(file):
        pass

    @staticmethod
    def copy_file(file: str, destination: str):
        cmd = ['rsync', '-a', file, destination]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

  # @staticmethod
  # # #temp for creating log and parameter tables
  # def session_start(connection):

  #     cursor = connection.cursor()
  #     # cursor.execute(statement)

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
                else:
                    pass

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
        for att_ctr in range(Backup.att_number):
            os.setxattr(file,
                        Backup.att_sum + '_' + str(att_ctr),
                        bytes(file_atts[0], 'utf-8'))
            os.setxattr(file,
                        Backup.att_time + '_' + str(att_ctr),
                        bytes(file_atts[1], 'utf-8'))

    def set_valid_atts(self):
        for att_ctr in range(Backup.att_number):
            Backup.valid_sum_atts.append(Backup.att_sum + '_' + str(att_ctr))
            Backup.valid_time_atts.append(Backup.att_time + '_' + str(att_ctr))

    @staticmethod
    def get_file_xatts(file: str):
        # this method splits the file's extended attribute list into the following:
        # - valid attributes - split into sum and time
        # - surplus attributes - starting with 'user.backup' but not valid
        # - other attributes - everything else -> not needed, skipping checks
        #
        # surplus attributes should be cleared by the end of the backup cycle

        # reading all at once to minimize data access
        xattr_list = os.listxattr(file)

        valid_sum_xatts = []
        valid_time_xatts = []
        surplus_xatts = []


        for xattr in xattr_list:
            if xattr in Backup.valid_sum_atts:
                valid_sum_xatts.append(xattr)
            elif xattr in Backup.valid_time_atts:
                valid_time_xatts.append(xattr)
            elif xattr.startswith('user.backup.'):
                surplus_xatts.append(xattr)

        return valid_sum_xatts, valid_time_xatts, surplus_xatts


    @staticmethod
    def clear_excess_file_atts(file: str, file_xatts: list):
        for xatt in file_xatts:
            os.removexattr(file, xatt)

    @staticmethod
    def clear_all_file_atts(file: str):
        pass

    @staticmethod
    def check_sum_validity(sum_att: str):
        if len(sum_att) != 128:
            return False
        # should we test for both conditions?
        elif not Backup.check_is_hex(sum_att):
            return False
        else:
            return True

    @staticmethod
    def check_is_hex(sum_att: str):
        try:
            int(sum_att, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_time_validity(time_att: str):

        # First check is to verify that nanosecond part of the string is
        # numeric. This is due to the Python's datetime lack of required accuracy.
        if re.fullmatch('^.{26}\d{3}.{6}$', time_att) is None:
            return False
        # Second check is to verify whether the rest of string is an actual
        # datetime.
        elif not Backup.check_is_datetime(time_att):
            return False
        else:
            return True

        #TODO: check whether date is probable

    @staticmethod
    def check_is_datetime(time_att: str):
        try:
            datetime.datetime.strptime(time_att[:27] + time_att[29:],
                                       '%Y-%m-%d %H:%M:%S.%f %z')
            return True
        except ValueError:
            return False

    # TODO boundaries
    # TODO sprawdzić kopiowanie atrybutów -> nie kopiują się
    # TODO timechange / timezone change
    # TODO whole messages instead of errors
