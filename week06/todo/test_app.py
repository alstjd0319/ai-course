import unittest
import os
import sqlite3
import sys

# Add current directory to sys.path so we can import app
sys.path.append(os.getcwd())

import app as app_module

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        # Use a separate test database
        self.test_db = 'test_database.db'
        app_module.DATABASE = self.test_db
        
        self.app = app_module.app.test_client()
        
        # Initialize test database
        with app_module.app.app_context():
            db = app_module.get_db()
            with open('schema.sql', 'r') as f:
                db.executescript(f.read())
            db.commit()

    def tearDown(self):
        # Remove test database
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except Exception:
                pass

    def test_get_index(self):
        """Test GET / returns 200 and displays a page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_todo(self):
        """Test POST /add adds a todo to the database."""
        response = self.app.post('/add', data={'title': 'Test Todo'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Todo', response.data)

        # Verify in DB
        db = app_module.get_db()
        res = db.execute('SELECT * FROM todo WHERE title = ?', ('Test Todo',)).fetchone()
        self.assertIsNotNone(res)
        self.assertEqual(res['title'], 'Test Todo')
        db.close()

    def test_add_empty_todo(self):
        """Test POST /add with empty title does not add anything."""
        response = self.app.post('/add', data={'title': ' '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        db = app_module.get_db()
        res = db.execute('SELECT COUNT(*) FROM todo').fetchone()
        self.assertEqual(res[0], 0)
        db.close()

if __name__ == '__main__':
    unittest.main()

import unittest
import os
import sqlite3
from app import app

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        # Use a separate test database
        self.test_db = 'test_database.db'
        app.config['DATABASE'] = self.test_db
        # Patch the DATABASE variable in the app module
        import app as app_module
        self.original_db = app_module.DATABASE
        app_module.DATABASE = self.test_db
        
        self.app = app.test_client()
        
        # Initialize test database
        with app.app_context():
            import app as app_module_inner
            # We need to manually initialize because init_db might check for existence
            # and we want to ensure it uses our test_db
            with app_module_inner.get_db() as db:
                # Clear if exists
                db.execute('DROP TABLE IF EXISTS todo')
                # Re-create
                with open('schema.sql', 'r') as f:
                    db.executescript(f.read())
                db.commit()

    def tearDown(self):
        # Restore original database setting
        import app as app_module
        app_module.DATABASE = self.original_db
        
        # Remove test database
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_get_index(self):
        """Test GET / returns 200 and displays a page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_todo(self):
        """Test POST /add adds a todo to the database."""
        response = self.app.post('/add', data={'title': 'Test Todo'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Todo', response.data)

        # Verify in DB
        import app as app_module
        with app_module.get_db() as db:
            res = db.execute('SELECT * FROM todo WHERE title = ?', ('Test Todo',)).fetchone()
            self.assertIsNotNone(res)
            self.assertEqual(res['title'], 'Test Todo')

    def test_add_empty_todo(self):
        """Test POST /add with empty title does not add anything."""
        response = self.app.post('/add', data={'title': ' '}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        import app as app_module
        with app_module.get_db() as db:
            res = db.execute('SELECT COUNT(*) FROM todo').fetchone()
            self.assertEqual(res[0], 0)

if __name__ == '__main__':
    unittest.main()
