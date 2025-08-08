import unittest
from src.persistence.storage import PersistenceManager
import pytest

@pytest.mark.skip(reason="Legacy PersistenceManager deprecated; persistence covered by service tests.")
def test_legacy_persistence_manager():
    assert True

class TestPersistenceManager(unittest.TestCase):

    def setUp(self):
        self.manager = PersistenceManager('test_data.json')

    def test_save_load(self):
        test_data = {'budget': {'food': 200, 'transport': 100}}
        self.manager.save(test_data)
        loaded_data = self.manager.load()
        self.assertEqual(test_data, loaded_data)

    def test_auto_save_on_change(self):
        initial_data = {'budget': {'food': 200, 'transport': 100}}
        self.manager.save(initial_data)
        self.manager.data['budget']['food'] = 150
        self.manager.auto_save()
        loaded_data = self.manager.load()
        self.assertEqual(loaded_data['budget']['food'], 150)

    def tearDown(self):
        import os
        if os.path.exists('test_data.json'):
            os.remove('test_data.json')

if __name__ == '__main__':
    unittest.main()