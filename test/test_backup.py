from unittest import TestCase
from unittest import main
from backup.backup.backup import Backup
from backup.test.test_file import TestFile
from backup.test.test_file import FileType

import os


# image flif bgp webp


class TestBackup(TestCase):
    """ TestBackup class """

    def setUp(self):
        file = TestFile('text_file.txt', FileType.text, '1k', 1)
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
