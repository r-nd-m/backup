import datetime
import os
import re
import subprocess


class File:
    """A file handler class"""

    # text declarations
    method = 'sha512sum'

    att_file_sum = 'user.backup.file_checksum'
    att_time = 'user.backup.st_mtime'
    att_image_sum = 'user.backup.image_checksum'

    def __init__(self):
        """Init method"""
        pass

    @staticmethod
    def analyze_file(file):
        file_attributes_calc = File.get_file_atts_calc(file)
        file_attributes_read = File.get_file_atts_read(file)[0:2]
        print(file_attributes_calc)
        print(file_attributes_read)

    @staticmethod
    def get_file_checksum_calc(file: str):
        # using external checksum commands due to performance considerations
        cmd = [File.method, file]
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
        return (File.get_file_checksum_calc(file),
                File.get_file_mtime_calc(file))

    @staticmethod
    def get_file_atts_read(file: str):
        # reading all at once to minimize data access
        xattr_list = os.listxattr(file)

        return xattr_list
#
#        for xattr in xattr_list:
#            att_sum_cur = File.att_file_sum
#            att_time_cur = File.
#
#            if xattr == att_sum_cur:
#                raw_attribute = os.getxattr(file, att_sum_cur)
#                file_attributes_sum[att] = \
#                    raw_attribute.decode(encoding='utf-8')
#            elif xattr == att_time_cur:
#                raw_attribute = os.getxattr(file, att_time_cur)
#                file_attributes_time[att] = \
#                    raw_attribute.decode(encoding='utf-8')
#            else:
#                pass
#
#        sum_most_common, error_level = \
#            File.get_most_common_att(file_attributes_sum)
#        time_most_common, error_level = \
#            File.get_most_common_att(file_attributes_time)
#
#        return (sum_most_common, time_most_common, error_level)

    @staticmethod
    def set_file_atts(file: str, file_atts: list):
        os.setxattr(file, File.att_file_sum, bytes(file_atts[0], 'utf-8'))
        os.setxattr(file, File.att_time, bytes(file_atts[1], 'utf-8'))

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
        return xattr_list

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
        elif not File.check_is_hex(sum_att):
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
        elif not File.check_is_datetime(time_att):
            return False
        else:
            return True

            # TODO: check whether date is probable
            # TODO timechange / timezone change

    @staticmethod
    def check_is_datetime(time_att: str):
        try:
            datetime.datetime.strptime(time_att[:27] + time_att[29:],
                                       '%Y-%m-%d %H:%M:%S.%f %z')
            return True
        except ValueError:
            return False
