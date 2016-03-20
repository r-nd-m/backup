from backup.backup.backup import Backup
from backup.test.converter import human2bytes
from enum import Enum
import array
import math
import os
import random
import string
import subprocess
import wave


class FileType(Enum):
    """ File type enumerator class """

    text = 'text'
    image = 'image'
    audio = 'audio'
    video = 'video'


class TestFile:
    """ Test file generation class """

    file_name = ''

    def __init__(self,
                 file_name: str,
                 file_type: Enum,
                 file_size: str,
                 file_seed: int,
                 arguments: list = None):

        self.file_name = file_name

        if file_type == FileType.text:
            byte_size = human2bytes(file_size)
            random.seed(file_seed)
            file = open(file_name, 'w')
            text = ''.join(
                random.choice(string.printable) for _ in range(byte_size))
            file.write(text)
            file.close()
        elif file_type == FileType.image:
            pass
        elif file_type == FileType.audio:
            pass
        elif file_type == FileType.video:
            pass
        else:
            pass

    def set_attributes(self):
        file_attributes_calc = Backup.get_file_atts_calc(self.file_name)
        Backup.set_file_atts(self.file_name, file_attributes_calc)

    def file_flip_bit(self, file_name: str):
        pass

    def attribute_flip_bit(self, attribute_name: str):
        pass

    def attribute_make_incorrect(self, attribute_name: str):
        pass

    @staticmethod
    def set_file_attribute(file: str, att_name: str, att_val: bytes):
        os.setxattr(file, att_name, att_val)

        # set mod date

        # create analog

        # single attribute

    def create_checksum(self):
        file = open(self.file_name + '.sum', 'w')
        checksum = Backup.get_file_checksum_calc(self.file_name)
        file.write(checksum)
        file.close()

    # TODO: fix method below
    @staticmethod
    def create_music_file(file):
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
