from unittest import TestCase
from unittest import main
from backup.file import File
from unittest import TestCase
from unittest import main
# from backup.backup.backup import Backup
#from backup.test.test_file import TestFile
#from backup.test.test_file import FileType
import subprocess

import os

# image flif bgp webp


class TestFile(TestCase):
    """ TestFile class """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_file_checksum_calc(self):
        file = TestFile('text_file.txt', FileType.text, '1k', 1)
        file.create_checksum()
        file.set_attributes()

        file_name = 'text_file.txt'
        checksum_calc = Backup.get_file_checksum_calc(file_name)
        sum_name = file_name + '.sum'
        file = open(sum_name)
        checksum_read = file.read().split(" ")[0]
        file.close()
        self.assertEqual(checksum_calc, checksum_read)
        os.remove('text_file.txt')
        os.remove('text_file.txt.sum')

    # TODO Test: verify checksum

    def test_get_file_mtime_calc(self):
        file_name = 'text_file.txt'
        mtime_calc = Backup.get_file_mtime_calc(file_name)
        mtime_read = Backup.get_file_atts_read(file_name)[1]
        print(Backup.get_file_xatts(file_name))
        print(mtime_calc, mtime_read)
        self.assertEqual(mtime_calc, mtime_read)

    def test_get_file_atts_calc(self):
        test_file = 'text_file.txt'
        file_attributes_calc = Backup.get_file_atts_calc(test_file)
        file_attributes_read = Backup.get_file_atts_read(test_file)[0:2]
        self.assertEqual(file_attributes_calc, file_attributes_read)

    def test_get_file_atts_read(self):
        test_file = 'text_file.txt'
        file_attributes_calc = Backup.get_file_atts_calc(test_file)
        file_attributes_read = Backup.get_file_atts_read(test_file)[0:2]
        Backup.check_sum_validity(file_attributes_calc[0])
        Backup.check_time_validity(file_attributes_calc[1])
        #cmd = ['rsync', '-a', 'opalinsp@localhost:/home/opalinsp/mac.jpg', '.']
        #p = subprocess.Popen(cmd,
        #                     stdout=subprocess.PIPE,
        #                     stderr=subprocess.PIPE)
        #out, err = p.communicate()
        #print(out, err)
        self.assertEqual(file_attributes_calc, file_attributes_read)

    def test_get_most_common_att(self):
        pass

    def test_set_file_atts(self):
        pass

    def test_clear_file_atts(self):
        pass

    def test_clear_file_att(self):
        pass

# def test_log_table_create(self):
#        Backup.backup_start(Backup)

from backup.test.test_file import TestFile
from backup.test.test_file import FileType
import subprocess

import os

# image flif bgp webp


class TestFile(TestCase):
    """ TestBackup class """

    def setUp(self):
        root = backup.config[Backup.sessions_config][0].source_directory
        file = CreateTestFile(root + 'text_file.txt', FileType.text, '1k', 1)
        file.create_checksum()
        file.set_attributes()

    def tearDown(self):
        os.remove('text_file.txt')
        os.remove('text_file.txt.sum')

    def test_get_file_checksum_calc(self):
        file_name = 'text_file.txt'
        checksum_calc = Backup.get_file_checksum_calc(file_name)
        sum_name = file_name + '.sum'
        file = open(sum_name)
        checksum_read = file.read().split(" ")[0]
        file.close()
        self.assertEqual(checksum_calc, checksum_read)

    # TODO Test: verify checksum

    def test_get_file_mtime_calc(self):
        file_name = 'text_file.txt'
        mtime_calc = Backup.get_file_mtime_calc(file_name)
        mtime_read = Backup.get_file_atts_read(file_name)[1]
        print(Backup.get_file_xatts(file_name))
        print(mtime_calc, mtime_read)
        self.assertEqual(mtime_calc, mtime_read)

    def test_get_file_atts_calc(self):
        test_file = 'text_file.txt'
        file_attributes_calc = Backup.get_file_atts_calc(test_file)
        file_attributes_read = Backup.get_file_atts_read(test_file)[0:2]
        self.assertEqual(file_attributes_calc, file_attributes_read)

    def test_get_file_atts_read(self):
        test_file = 'text_file.txt'
        file_attributes_calc = Backup.get_file_atts_calc(test_file)
        file_attributes_read = Backup.get_file_atts_read(test_file)[0:2]
        Backup.check_sum_validity(file_attributes_calc[0])
        Backup.check_time_validity(file_attributes_calc[1])
        #cmd = ['rsync', '-a', 'opalinsp@localhost:/home/opalinsp/mac.jpg', '.']
        #p = subprocess.Popen(cmd,
        #                     stdout=subprocess.PIPE,
        #                     stderr=subprocess.PIPE)
        #out, err = p.communicate()
        #print(out, err)
        self.assertEqual(file_attributes_calc, file_attributes_read)

    def test_get_most_common_att(self):
        pass

    def test_set_file_atts(self):
        pass

    def test_clear_file_atts(self):
        pass

    def test_clear_file_att(self):
        pass

# def test_log_table_create(self):
#        Backup.backup_start(Backup)
