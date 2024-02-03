#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        pass

    def test_pep8_conformance_db_storage(self):
        """Test that db_storage.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0)

    def test_pep8_conformance_test_db_storage(self):
        """Test that test_db_storage.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0)

    def test_db_storage_module_docstring(self):
        """Test for the presence of docstrings in db_storage module."""
        self.assertIsNot(db_storage.__doc__, None)
        self.assertTrue(len(db_storage.__doc__) >= 1)

    def test_db_storage_class_docstring(self):
        """Test for the presence of docstrings in DBStorage class."""
        self.assertIsNot(DBStorage.__doc__, None)
        self.assertTrue(len(DBStorage.__doc__) >= 1)

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods."""
        for func in dir(DBStorage):
            self.assertIsNot(getattr(DBStorage, func).__doc__, None)
            self.assertTrue(len(getattr(DBStorage, func).__doc__) >= 1)


class TestDBStorage(unittest.TestCase):
    # ...

    def test_all_method_with_class(self):
        """Test the all method with a specific class."""
        storage = DBStorage()
        storage.reload()
        all_states = storage.all(State)
        self.assertIsInstance(all_states, dict)
        for obj in all_states.values():
            self.assertIsInstance(obj, State)

    def test_new_method(self):
        """Test the new method."""
        storage = DBStorage()
        state = State(name="California")
        storage.new(state)
        self.assertIn(state, storage._DBStorage__session)

    def test_save_method(self):
        """Test the save method"""
        storage = DBStorage()
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertIn(state, storage._DBStorage__session)

    def test_delete_method(self):
        """Test the delete method"""
        storage = DBStorage()
        state = State(name="California")
        storage.new(state)
        storage.save()
        storage.delete(state)
        self.assertNotIn(state, storage._DBStorage__session)

    def test_reload_method(self):
        """Test the reload method"""
        storage = DBStorage()
        state = State(name="California")
        storage.new(state)
        storage.save()
        storage.reload()
        self.assertNotIn(state, storage._DBStorage__session)

    def test_close_method(self):
        """Test the close method"""
        storage = DBStorage()
        storage.close()
        self.assertIsNone(storage._DBStorage__session)

    def test_get_method(self):
        """Test the get method"""
        storage = DBStorage()
        state = State(name="California")
        storage.new(state)
        storage.save()
        retrieved_state = storage.get(State, state.id)
        self.assertEqual(retrieved_state, state)

    def test_count_method_with_class(self):
        """Test the count method with a specific class"""
        storage = DBStorage()
        storage.reload()
        count = storage.count(State)
        self.assertEqual(count, len(storage.all(State)))
