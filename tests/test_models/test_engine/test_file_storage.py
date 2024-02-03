#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        cls.storage = FileStorage()

    def setUp(self):
        """Set up test method"""
        self.storage.reload()

    def tearDown(self):
        """Clean up after each test method"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attribute"""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertIs(all_objects, self.storage._FileStorage__objects)

    def test_new(self):
        """Test that new adds an object to the FileStorage.__objects attribute"""
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        self.storage.new(obj)
        self.assertIn(obj_key, self.storage._FileStorage__objects)

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        self.storage.new(obj)
        self.storage.save()
        with open("file.json", "r") as f:
            data = json.load(f)
        self.assertIn(obj_key, data)

    def test_reload(self):
        """Test that reload properly reloads objects from file.json"""
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        self.assertIn(obj_key, self.storage._FileStorage__objects)

    def test_delete(self):
        """Test that delete properly deletes an object from FileStorage.__objects"""
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        self.storage.new(obj)
        self.storage.delete(obj)
        self.assertNotIn(obj_key, self.storage._FileStorage__objects)

    def test_close(self):
        """Test that close properly calls reload method"""
        with unittest.mock.patch('models.engine.file_storage.FileStorage.reload') as mock_reload:
            self.storage.close()
            mock_reload.assert_called_once()

    def test_get(self):
        """Test that get returns the object with the specified class and id"""
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        self.storage.new(obj)
        self.assertEqual(obj, self.storage.get(BaseModel, obj.id))
        self.assertIsNone(self.storage.get(BaseModel, "nonexistent_id"))

    def test_count(self):
        """Test that count returns the number of objects in FileStorage.__objects"""
        self.assertEqual(len(self.storage.all()), self.storage.count())
        obj = BaseModel()
        self.assertEqual(len(self.storage.all()), self.storage.count())
        self.storage.new(obj)
        self.assertEqual(len(self.storage.all()), self.storage.count())


if __name__ == '__main__':
    unittest.main()
