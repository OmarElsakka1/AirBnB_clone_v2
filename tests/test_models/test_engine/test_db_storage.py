#!/usr/bin/python
"""This is the unittesting for DBStorage class for AirBnb_Clone_v2"""
import unittest
import pep8
import os
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import MySQLdb


@unittest.skipIf(
       os.getenv('HBNB_TYPE_STORAGE') != 'db',
       "This test only work in DBStorage")
class TestDBStorage(unittest.TestCase):
    """this will test the DBStorage"""

    @classmethod
    def setUpClass(cls):
        """Setting up the Tests"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """This is teardown for the testing"""
        del cls.user

    def tearDown(self):
        """teardown as a method"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_DBStorage(self):
        """Testing pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        pep = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(pep.total_errors, 0, "fix pep8")

    def test_all(self):
        """testing if all works in DB Storage"""
        storage = FileStorage()
        objec = storage.all()
        self.assertIsNotNone(objec)
        self.assertEqual(type(objec), dict)
        self.assertIs(objec, storage._FileStorage__objects)

    def test_new(self):
        """testing in case new one was created"""
        storage = FileStorage()
        objec = storage.all()
        user_new = User()
        user_new.id = 123455
        user_new.name = "Kevin"
        storage.new(user_new)
        key = user_new.__class__.__name__ + "." + str(user_new.id)
        self.assertIsNotNone(objec[key])

    def test_reload_dbtorage(self):
        """
        test reloading
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as r:
            lines = r.readlines()
        try:
            os.remove(path)
        except Exception:
            pass
        self.storage.save()
        with open(path, 'r') as r:
            lines2 = r.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except Exception:
            pass
        with open(path, "w") as w:
            w.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)


if __name__ == "__main__":
    unittest.main()
