
import os
import unittest
 
from project import app, db
from project.models import User, Sneaker

 
TEST_DB = 'test.db'

class ProjectTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.create_all()
 
        self.assertEquals(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
 
    ########################
    #### helper methods ####
    ########################
 
    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )
    
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
    
    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
    
    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
    
    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)
    
    def add_sneakers(self):
        self.register_user()
        user1 = User.query.filter_by(email='patkennedy79@gmail.com').first()
        sneaker1 = Sneaker('Yeezy1', 10000, user1.id, True)
        sneaker2 = Sneaker('Yeezy2', 12000, user1.id, True)
        sneaker3 = Sneaker('Yeezy3', 15000, user1.id, False)
        sneaker4 = Sneaker('Yeezy4', 18000, user1.id, False)
        db.session.add(sneaker1)
        db.session.add(sneaker2)
        db.session.add(sneaker3)
        db.session.add(sneaker4)
        db.session.commit()
    
 
    ###############
    #### tests ####
    ###############
 
    def test_main_page(self):
        self.register_user()
        self.add_sneakers()
        self.logout_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sneaker Shelf', response.data)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Yeezy1', response.data)
        self.assertIn(b'Yeezy2', response.data)
        # self.assertIn(b'Yeezy3', response.data)
        # self.assertIn(b'Yeezy4', response.data)

    def test_user_sneakers_page(self):
        self.register_user()
        self.add_sneakers()
        response = self.app.get('/sneakers', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sneaker Shelf', response.data)
        self.assertIn(b'Yeezy1', response.data)
        self.assertIn(b'Yeezy2', response.data)
        self.assertIn(b'Yeezy3', response.data)
        self.assertIn(b'Yeezy4', response.data)

    def test_user_sneakers_page_without_login(self):
        response = self.app.get('/sneakers', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fsneakers', response.data)
    
    def test_add_sneaker_page(self):
        self.register_user()
        response = self.app.get('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a New Sneaker', response.data)

    def test_add_sneaker(self):
        self.register_user()
        response = self.app.post(
            '/add',
            data=dict(sneaker_model_name='Yeezy',
                      sneaker_retail_price=15000),
            follow_redirects=True)
        self.assertIn(b'New sneaker, Yeezy, added!', response.data)
 
    def test_add_invalid_sneaker(self):
        self.register_user()
        response = self.app.post(
            '/add',
            data=dict(sneaker_model_name='Yeezy',
                      sneaker_retail_price='Delicious'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Sneaker was not added.', response.data)
        self.assertIn(b'This field is required.', response.data)
 

if __name__ == "__main__":
    unittest.main()