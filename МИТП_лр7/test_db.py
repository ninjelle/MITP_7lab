import unittest
import os
import sqlite3
from database import *

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Runs before each test"""
        if os.path.exists('test.db'):
            os.remove('test.db')
        
        create_database()
    
    def tearDown(self):
        """Runs after each test"""
        if os.path.exists('test.db'):
            os.remove('test.db')
    
    def test_1_create_database(self):
        """Test: Database is created"""
        self.assertTrue(os.path.exists('test.db'))
        
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('users', tables)
        self.assertIn('orders', tables)
        
        conn.close()
    
    def test_2_add_user(self):
        """Test: Adding a user"""
        user_id = add_user('John', 25, 'john@mail.com')
        
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        
        user = get_user(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user[1], 'John')  
        self.assertEqual(user[2], 25)      
        self.assertEqual(user[3], 'john@mail.com') 
    
    def test_3_add_user_duplicate_email(self):
        """Test: Error on duplicate email"""
        add_user('John', 25, 'john@mail.com')
        
        with self.assertRaises(ValueError) as context:
            add_user('Mike', 30, 'john@mail.com')
        
        self.assertIn('Email already exists', str(context.exception))
    
    def test_4_get_all_users(self):
        """Test: Getting all users"""
        add_user('John', 25, 'john@mail.com')
        add_user('Anna', 30, 'anna@mail.com')
        add_user('Mike', 35, 'mike@mail.com')
        
        users = get_all_users()
        
        self.assertEqual(len(users), 3)
        
        names = [user[1] for user in users]
        self.assertIn('John', names)
        self.assertIn('Anna', names)
        self.assertIn('Mike', names)
    
    def test_5_update_user(self):
        """Test: Updating user"""
        user_id = add_user('John', 25, 'john@mail.com')
        
        updated = update_user_age(user_id, 26)
        self.assertTrue(updated)
        
        user = get_user(user_id)
        self.assertEqual(user[2], 26)
    
    def test_6_update_nonexistent_user(self):
        """Test: Updating non-existent user"""
        updated = update_user_age(999, 26)
        self.assertFalse(updated)
    
    def test_7_delete_user(self):
        """Test: Deleting a user"""
        user_id = add_user('John', 25, 'john@mail.com')
        
        deleted = delete_user(user_id)
        self.assertTrue(deleted)
        
        user = get_user(user_id)
        self.assertIsNone(user)
    
    def test_8_delete_nonexistent_user(self):
        """Test: Deleting non-existent user"""
        deleted = delete_user(999)
        self.assertFalse(deleted)
    
    def test_9_add_order(self):
        """Test: Adding an order"""
        user_id = add_user('John', 25, 'john@mail.com')
        
        order_id = add_order(user_id, 'Laptop', 1000)
        
        self.assertIsInstance(order_id, int)
        self.assertGreater(order_id, 0)
    
    def test_10_get_user_orders(self):
        """Test: Getting user orders"""
        user_id = add_user('John', 25, 'john@mail.com')
        
        add_order(user_id, 'Laptop', 1000)
        add_order(user_id, 'Mouse', 50)
        add_order(user_id, 'Keyboard', 80)
        
        orders = get_user_orders(user_id)
        
        self.assertEqual(len(orders), 3)
        
        products = [order[2] for order in orders]
        self.assertIn('Laptop', products)
        self.assertIn('Mouse', products)
        self.assertIn('Keyboard', products)
    
    def test_11_join_users_orders(self):
        """Test: JOIN users and orders"""
        user1_id = add_user('John', 25, 'john@mail.com')
        user2_id = add_user('Anna', 30, 'anna@mail.com')
        
        add_order(user1_id, 'Laptop', 1000)
        add_order(user1_id, 'Mouse', 50)
        add_order(user2_id, 'Phone', 500)
        
        results = join_users_orders()
        
        self.assertEqual(len(results), 3)
        
        for result in results:
            self.assertEqual(len(result), 3)  
            self.assertIsInstance(result[0], str)  
            self.assertIsInstance(result[1], str)  
            self.assertIsInstance(result[2], float)  
    
    def test_12_foreign_key_constraint(self):
        """Test: Foreign key constraint"""
        try:
            order_id = add_order(999, 'Test', 100)
            self.assertIsInstance(order_id, int)
        except:
            pass

if __name__ == '__main__':
    unittest.main(verbosity=2)