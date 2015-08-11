# import queue
# import threading
import subprocess
import os


class Backup:
    """Backup class"""
    source_directory = []
    destination_directory = []
    omit_rules = []
    method = 'sha512sum'

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

    def get_file_checksum_ext(self, root, filename):
        cmd = [self.method, os.path.join(root, filename)]
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        checksum = out.decode(encoding='utf-8').split(" ")[0]
        return checksum

    def get_file_checksum_int(self, root, filename):
        pass
