import unittest
from backup import backup


class TestBackup(unittest.TestCase):
    """ TestBackup class """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_file_checksum_ext(self):
        test_checksum_part_1 = 'ef745a8d8995087fc1f1125b498393ae'
        test_checksum_part_2 = 'd765795e9ac6f4c50712cac9f59370df'
        test_checksum_part_3 = 'f5d8cd71457d7778bec1e9dcc718d1f0'
        test_checksum_part_4 = 'a2d1fa94659f6ffb6083549da6316334'
        test_checksum = ''.join([test_checksum_part_1, test_checksum_part_2,
                                 test_checksum_part_3, test_checksum_part_4])
        root = 'tests/test_backup_files'
        filename = 'testfile.txt'
        checksum = backup.Backup().get_file_checksum_ext(root, filename)
        self.assertEqual(test_checksum, checksum)


if __name__ == '__main__':
    unittest.main()
