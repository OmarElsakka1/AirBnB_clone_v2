#!/usr/bin/python3
"""Provide tests for console.py."""
import os
import pep8
import unittest
import models
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """This is for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """Setting up HBNBCommand, which is

        1) Rename -Temporarily- any existing file.json.
        2) Resetting FileStorage objects dictionary.
        3) Creating an instance of the command interpreter.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """HBNBCommand testing tearingdown.

        1) Restoring original file.json.
        2) Deleting the test HBNBCommand instance.
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()

    def setUp(self):
        """Reseting FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Deleting any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_pep8(self):
        """Testing Pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p_checking = style.check_files(["console.py"])
        self.assertEqual(p_checking.total_errors, 0, "fix Pep8")

    def test_docstrings(self):
        """Checking for docstrings."""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Testing empty line input."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("\n")
            self.assertEqual("", w.getvalue())

    def test_quit(self):
        """Testing quit command input."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("quit")
            self.assertEqual("", w.getvalue())

    def test_EOF(self):
        """Testing quitting of EOF."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.assertTrue(self.HBNB.onecmd("EOF"))

    def test_create_errors(self):
        """Test creating command errors."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create(self):
        """Testing create command."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create User")
            user = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create State")
            state = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create Place")
            place = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create City")
            city = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create Review")
            review = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("create Amenity")
            amenity = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all User")
            self.assertIn(user, w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all State")
            self.assertIn(state, w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all Place")
            self.assertIn(place, w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all City")
            self.assertIn(city, w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all Review")
            self.assertIn(review, w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(amenity, w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_kwargs(self):
        """Testing create command with kwargs."""
        with patch("sys.stdout", new=StringIO()) as w:
            call = ('create Place city_id="0001" name="My_house" '
                    'number_rooms=4 latitude=37.77 longitude=a')
            self.HBNB.onecmd(call)
            place = w.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all Place")
            out = w.getvalue()
            self.assertIn(place, out)
            self.assertIn("'city_id': '0001'", out)
            self.assertIn("'name': 'My house'", out)
            self.assertIn("'number_rooms': 4", out)
            self.assertIn("'latitude': 37.77", out)
            self.assertNotIn("'longitude'", out)

    def test_show(self):
        """Testing show command."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", w.getvalue())

    def test_destroy(self):
        """Testing destroy command input."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_all(self):
        """Testing all command input."""
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all State")
            self.assertEqual("[]\n", w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """Testing update command input."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("all User")
            objec = w.getvalue()
        my_id = objec[objec.find('(')+1:objec.find(')')]
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_z_all(self):
        """Testing alternate all command."""
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch("sys.stdout", new=StringIO()) as w:
            self.HBNB.onecmd("State.all()")
            self.assertEqual("[]\n", w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_z_count(self):
        """Testing count command inpout"""
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("State.count()")
            self.assertEqual("0\n", w.getvalue())

    def test_z_show(self):
        """Testing alternate show command inpout"""
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", w.getvalue())

    def test_destroy(self):
        """Testing alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", w.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """Testing alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("sldkfjsl.update()")
            self.assertEqual(
                "** class doesn't exist **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("all User")
            objec = w.getvalue()
        my_id = objec[objec.find('(')+1:objec.find(')')]
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", w.getvalue())
        with patch('sys.stdout', new=StringIO()) as w:
            self.HBNB.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", w.getvalue())


if __name__ == "__main__":
    unittest.main()
