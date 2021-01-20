
import os
import unittest
 
from project import app, db
 
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
 
 
 
    ###############
    #### tests ####
    ###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Sneaker Shelf', response.data)
        self.assertIn(b'Adidas', response.data)
        self.assertIn(b'Nike', response.data)
        self.assertIn(b'Add Sneaker', response.data)

    def test_main_page_query_results(self):
        response = self.app.get('/add', follow_redirects=True)
        self.assertIn(b'Add a New Sneaker', response.data)

    def test_add_sneaker(self):
        response = self.app.post(
            '/add',
            data=dict(sneaker_model_name='Yeezy',
                      sneaker_retail_price=15000),
            follow_redirects=True)
        self.assertIn(b'New sneaker, Yeezy, added!', response.data)
 
    def test_add_invalid_recipe(self):
        response = self.app.post(
            '/add',
            data=dict(sneaker_model_name='Yeezy',
                      sneaker_retail_price='Delicious'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Sneaker was not added.', response.data)
        self.assertIn(b'This field is required.', response.data)
 

if __name__ == "__main__":
    unittest.main()