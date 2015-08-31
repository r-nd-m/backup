import queue
import threading
import subprocess
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

    def get_file_checksum(self, file):
        # using external checksum commands due to performance considerations
        cmd = [self.method, file]
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
