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
        pass

    def test_pep8_conformance_file_storage(self):
        """Test that file_storage.py conforms to PEP8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found")

    def test_pep8_conformance_test_file_storage(self):
        """Test that test_file_storage.py conforms to PEP8 style"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found")

    def test_file_storage_module_docstring(self):
        """Test that file_storage.py has a docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py should have a docstring")

    def test_file_storage_class_docstring(self):
        """Test that FileStorage class has a docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class should have a docstring")

    def test_fs_func_docstrings(self):
        """Test that all functions in FileStorage have docstrings"""
        for func in dir(FileStorage):
            if callable(getattr(FileStorage, func)):
                self.assertIsNot(getattr(FileStorage, func).__doc__, None,
                                 f"{func} method in FileStorage class should have a docstring")


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """Test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload(self):
        """Test that reload properly reloads objects from file.json"""
        storage = FileStorage()
        storage.reload()
        self.assertEqual(type(storage.all()), dict)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """Test that delete properly deletes an object from __objects"""
        storage = FileStorage()
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        storage.new(obj)
        storage.delete(obj)
        self.assertNotIn(obj_key, storage.all())

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_close(self):
        """Test that close properly calls reload method"""
        storage = FileStorage()
        storage.reload = MagicMock()
        storage.close()
        storage.reload.assert_called_once()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get returns the object with the given class and id"""
        storage = FileStorage()
        obj = BaseModel()
        obj_key = obj.__class__.__name__ + "." + obj.id
        storage.new(obj)
        self.assertEqual(storage.get(BaseModel, obj.id), obj)
        self.assertIsNone(storage.get(BaseModel, "nonexistent_id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count returns the number of objects of a given class"""
        storage = FileStorage()
        self.assertEqual(storage.count(), len(storage.all()))
        self.assertEqual(storage.count(BaseModel), len(storage.all(BaseModel)))
