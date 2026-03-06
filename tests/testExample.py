from kissut import LoggingTestCase
import os


# all test classes must derive from unittest.TestCase, which LoggingTestCase does...
# class TestExample(object):
class TestExample(LoggingTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # this will run only once upon instantiating the class
        # do stuff here...
        cls.cfg = cls.getConfig()

    def test_a_isTrue(self):
        s = self.randString()
        self.logger.debug("s: {}".format(s))
        self.assertTrue(s)

    def test_b_saveWorkData(self):
        self.cfg["data"] = "testData.json"
        fqfn = self.dumpWkDirData(data={"a": "b"}, filename=self.cfg["data"])
        self.logger.debug("file name: {}".format(self.cfg["data"]))
        self.assertTrue(os.path.exists(fqfn))

    def test_c_isPresent(self):
        self.logger.debug("cfg: {}".format(self.cfg))
        d = self.loadWkDirData(self.cfg["data"])
        self.logger.debug("data: {}".format(d))
        self.assertIsNotNone(d)
