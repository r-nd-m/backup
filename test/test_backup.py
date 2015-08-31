import os
import unittest
from backup import backup


class TestBackup(unittest.TestCase):

    """ TestBackup class """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_file_checksum(self):
        root = 'test_backup_files'
        test_file_name = 'textfile.txt'
        test_file = os.path.join(root, test_file_name)
        checksum_calc = backup.Backup().get_file_checksum(test_file)
        test_file_sum_name = 'textfile.txt.sum'
        test_file_sum = os.path.join(root, test_file_sum_name)
        f = open(test_file_sum)
        checksum_read = f.read().split(" ")[0]
        f.close()
        self.assertEqual(checksum_calc, checksum_read)

    def test_get_file_attributes(self):
        root = 'test_backup_files'
        test_file_name = 'flacfile.flac'
        test_file = os.path.join(root, test_file_name)
        file_attributes_calc = backup.Backup().get_file_attributes_calc(test_file)
        # backup.Backup().set_file_attributes(test_file, file_attributes_calc)
        file_attributes_read = backup.Backup().get_file_attributes_read(test_file)
        self.assertEqual(file_attributes_calc, file_attributes_read)

if __name__ == '__main__':
    unittest.main()
