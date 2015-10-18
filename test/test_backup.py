from unittest import TestCase
from unittest import main
from backup import backup
import array
import math
import os
import random
import sqlite3
import string
import subprocess
import wave


class TestBackup(TestCase):
    """ TestBackup class """

    @staticmethod  # broken and unused for now
    def create_flac_file(file):
        # create files for testing
        duration = 1  # seconds
        freq = 440  # of cycles per second (Hz) (frequency of the sine waves)
        volume = 100  # percent
        data = array.array('h')  # signed short integer (-32768 to 32767) data
        sample_rate = 44100  # of samples per second (standard)
        num_chan = 1  # of channels (1: mono, 2: stereo)
        # 2 bytes because of using signed short integers => bit depth = 16
        data_size = 2
        num_sample_per_cyc = int(sample_rate / freq)
        num_samples = sample_rate * duration
        for i in range(num_samples):
            sample = 32767 * float(volume) / 100
            sample *= math.sin(math.pi * 2 * (i % num_sample_per_cyc) /
                               num_sample_per_cyc)
            data.append(int(sample))
        f = wave.open(file, 'w')
        f.setparams((num_chan, data_size, sample_rate, num_samples, "NONE",
                     "Uncompressed"))
        f.writeframes(data.tobytes())
        f.close()
        p = subprocess.Popen(["flac", file])
        p.communicate()

    @staticmethod
    def create_sample_text_file(file_name, size, seed):
        random.seed(seed)
        file = open(file_name, 'w')
        text = ''.join(random.choice(string.printable) for _ in range(size))
        file.write(text)
        file.close()
        file_attributes_calc = backup.Backup.get_file_attributes_calc(file_name)
        backup.Backup().set_file_attributes(file_name, file_attributes_calc)


    @staticmethod
    def create_file_checksum(file_name):
        file = open(file_name + '.sum', 'w')
        sum = backup.Backup.get_file_checksum(file_name)
        file.write(sum)
        file.close()

    def setUp(self):
        self.create_sample_text_file('textfile.txt', 128, 1)
        self.create_file_checksum('textfile.txt')

    def tearDown(self):
        os.remove('textfile.txt')
        os.remove('textfile.txt.sum')

    def test_get_file_checksum(self):
        test_file = 'textfile.txt'
        checksum_calc = backup.Backup.get_file_checksum(test_file)
        test_file_sum = test_file + '.sum'
        file = open(test_file_sum)
        checksum_read = file.read().split(" ")[0]
        file.close()
        self.assertEqual(checksum_calc, checksum_read)

    def test_get_file_attributes(self):
        test_file = 'textfile.txt'
        file_attributes_calc = backup.Backup.get_file_attributes_calc(test_file)
        file_attributes_read = backup.Backup.get_file_attributes_read(test_file)
        self.assertEqual(file_attributes_calc, file_attributes_read)

    def test_log_table_create(self):
        conn = sqlite3.connect('example.db')
        backup.Backup.log_table_create(conn, 'Session')
        backup.Backup.log_table_create(conn, 'File')
        backup.Backup.log_table_create(conn, 'Iteration')
        backup.Backup.log_table_create(conn, 'Parameter')
        conn.close()

if __name__ == '__main__':
    main()
