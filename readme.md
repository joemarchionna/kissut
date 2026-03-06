# kissut - Python Unittesting Utilities

Provides a simple automatic test case that sets up a new log each time tests are run. Also provides
some basic methods to assist with configuration and file management when running tests

## Usage

Installation:

````bash
    pip install kissut
````

LoggingTestCase subclasses unittest.TestCase, so when creating your tests, simply subclass LoggingTestCase instead of 
TestCase. LoggingTestCase sets up a unittest directory wkdir/unittest/ and saves log directories there:

````python
from kissut import LoggingTestCase
import os

# all test classes must derive from unittest.TestCase, which LoggingTestCase does...
class TestExample(LoggingTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # this loads the test configuration file
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
````

This produces the following directory structure after running it twice (the first time will abort as it creates the config file):

````text
<project folder>
└── wkdir
    └── unittest
        ├── 20260306T155251
        │   └── log.txt
        ├── 20260306T160132
        │   ├── log.txt
        │   └── testData.json
        └── testConfig.json
````

Obviously loading a config file in the setUpClass method is not required, it is just something I find useful, especially when a connection string or url is required for testing.

Some additional things to note, a simple random string method is included, as are dump and save methods for data to the working directory, and an initialized logger on the test case object.

If you prefer to save the logs or test config in another location, create a session-specific or user environment variable that defines path to the alternative configuration file. The contents of the alternative configuration file should be formatted like the following, obviously replacing the values as appropriate:

````json
{
    "logCfgFile": "wkdir/alt_unittest/logConfig.json",
    "testCfgFile": "wkdir/alt_unittest/testConfig.json"
}
````

## Cloning For Development

Set up a virtual environment. Once an environment is set up, activate it and add dependencies with the following:

````bash
    pip install -r requirements/dev.txt
````

The dev.txt file includes:

* BLACK, a code formatter, see notes at the bottom of this file for details
* build, which provides the support for the building of the package

### To run tests:

````bash
    python -m unittest discover -s tests/
````

The run the following to confirm the alternative configuration works, ensuring the unittest configuration and log directories get saved in the wkdir/alt_unittest directory:

````bash
    export KISSUT_CFG_FILE="tests/altConfig.json"
    python -m unittest discover -s tests/
````

### Code Formatting

Code formatting is done using BLACK. BLACK allows almost no customization to how code is formatted with the exception of line length, which has been set to 119 characters.

Use the following to bulk format files:


````bash
    black . -l 144
````

### Creating A New Release

Please do the following when making a new release, most are documented above:

1. Run tests
1. Code format
1. Be sure to update the change log and _metadata.json with version and notes
1. git add, commit, and push changes
1. run the following code to generate a wheel:

````bash
    python -m build
````
