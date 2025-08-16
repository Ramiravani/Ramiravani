import json
import os
from datetime import datetime
from config import DATABASE_FILE

class Database:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.data = self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'users': {},
                'products': {},
                'orders': {},
                'categories': {}
            }
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, user_id, username=None, first_name=None):
        """Add or update user"""
        self.data['users'][str(user_id)] = {
            'username': username,
            'first_name': first_name,
            'joined_at': datetime.now().isoformat(),
            'is_admin': False
        }
        self.save_data()
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.data['users'].get(str(user_id))
    
    def add_product(self, product_id, name, description, price, category, image_url=None):
        """Add product"""
        self.data['products'][product_id] = {
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'image_url': image_url,
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        self.save_data()
    
    def get_products(self, category=None):
        """Get all products or by category"""
        products = self.data['products']
        if category:
            return {k: v for k, v in products.items() if v['category'] == category and v['active']}
        return {k: v for k, v in products.items() if v['active']}
    
    def get_product(self, product_id):
        """Get product by ID"""
        return self.data['products'].get(product_id)
    
    def add_order(self, order_id, user_id, product_id, payment_method):
        """Add order"""
        product = self.get_product(product_id)
        if product:
            self.data['orders'][order_id] = {
                'user_id': user_id,
                'product_id': product_id,
                'product_name': product['name'],
                'price': product['price'],
                'payment_method': payment_method,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            self.save_data()
            return True
        return False
    
    def get_orders(self, user_id=None):
        """Get orders by user or all orders"""
        orders = self.data['orders']
        if user_id:
            return {k: v for k, v in orders.items() if v['user_id'] == user_id}
        return orders
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        if order_id in self.data['orders']:
            self.data['orders'][order_id]['status'] = status
            self.save_data()
            return True
        return False

# Initialize database instance
db = Database()

