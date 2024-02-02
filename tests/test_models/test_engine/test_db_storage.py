import unittest
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import inspect
import pep8
import models


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up class"""
        cls.storage = DBStorage()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(self.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        objs = self.storage.all()
        self.assertEqual(len(objs), 0)

        obj = BaseModel()
        obj.save()
        objs = self.storage.all()
        self.assertIn(obj, objs.values())

    def test_new(self):
        """Test that new adds an object to the database"""
        obj = BaseModel()
        self.assertNotIn(obj, self.storage.all().values())
        self.storage.new(obj)
        self.assertIn(obj, self.storage.all().values())

    def test_save(self):
        """Test that save properly saves objects to the database"""
        obj = BaseModel()
        obj.save()
        self.assertIn(obj, self.storage.all().values())

    def test_delete(self):
        """Test that delete removes an object from the database"""
        obj = BaseModel()
        obj.save()
        self.assertIn(obj, self.storage.all().values())
        self.storage.delete(obj)
        self.assertNotIn(obj, self.storage.all().values())

    def test_reload(self):
        """Test that reload properly reloads objects from the database"""
        obj = BaseModel()
        obj.save()
        self.assertIn(obj, self.storage.all().values())

        self.storage.reload()
        self.assertNotIn(obj, self.storage.all().values())

    def test_get(self):
        """Test that get retrieves an object from the database"""
        obj = BaseModel()
        obj.save()
        retrieved_obj = self.storage.get(BaseModel, obj.id)
        self.assertEqual(obj, retrieved_obj)

    def test_count(self):
        """Test that count returns the number of objects in the database"""
        count = self.storage.count()
        self.assertEqual(count, 0)

        obj = BaseModel()
        obj.save()
        count = self.storage.count()
        self.assertEqual(count, 1)


if __name__ == '__main__':
    unittest.main()
