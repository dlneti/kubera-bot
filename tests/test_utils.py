import unittest
from datetime import datetime

import utils

class TestConvertTimestamp(unittest.TestCase):
    def test_returns_datetime(self):
        """
        it returns datetime object
        """

        timestamp = datetime.timestamp(datetime.now())
        result = utils.convert_timestamp(timestamp)
        self.assertIsInstance(result, datetime)
    def test_returns_list_of_datetimes(self):
        """
        it returns correct list of datetime objects
        """

        timestamps = [datetime.timestamp(datetime.now()) for i in range(10)]
        result = utils.convert_timestamp(timestamps)
        self.assertIsInstance(result, list)
        self.assertEquals(len(result), len(timestamps))
        
        # all results are datetime
        for r in result:
            self.assertIsInstance(r, datetime)

    def test_timestamp_transform(self):
        """
        it converts the timestamp to seconds if it was passed in ms
        """
        now = datetime.now()
        timestamp_ms = int(datetime.timestamp(now)) * 1000
        timestamp_s = int(datetime.timestamp(now))
        result_ms = utils.convert_timestamp(timestamp_ms)
        result_s = utils.convert_timestamp(timestamp_s)
        self.assertEquals(result_ms.year, now.year)
        self.assertEquals(result_s.year, now.year)


if __name__ == "__main__":
    unittest.main()