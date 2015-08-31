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

    def backup_start():
        pass

    def create_database_log1():
        pass

    def create_database_log2():
        pass

    def get_files():
        pass

    def log():
        pass

    def check():
        pass

    def get_file_checksum(self, file):
        # using external checksum commands due to performance considerations
        cmd = [self.method, file]
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
        return(checksum)

    def get_file_mtime(self, file):
        # using external mtime command due to issues with Python's float
        # accuracy and lack of proper timezone formatting
        cmd = ['stat', '--format=%y', file]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        mtime = out.decode(encoding='utf-8').split("\n")[0]
        return(mtime)

    def get_file_attributes_calc(self, file):
        file_attributes = [None]*2
        file_attributes[0] = self.get_file_checksum(file)
        file_attributes[1] = self.get_file_mtime(file)
        return(file_attributes)

    def get_file_attributes_read(self, file):
        xattr_list = os.listxattr(file)
        file_attributes = [None]*2
        for xattr in xattr_list:
            if xattr == self.att_sum:
                raw_attribute = os.getxattr(file, self.att_sum)
                file_attributes[0] = raw_attribute.decode(encoding='utf-8')
            elif xattr == self.att_time:
                raw_attribute = os.getxattr(file, self.att_time)
                file_attributes[1] = raw_attribute.decode(encoding='utf-8')
        return(file_attributes)

    def set_file_attributes(self, file, file_attributes):
        os.setxattr(file, self.att_sum, file_attributes[0])
        os.setxattr(file, self.att_time, file_attributes[1])
