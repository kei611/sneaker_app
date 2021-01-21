from project import db
from project.models import Sneaker,User


# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

sneaker1 = Sneaker('adidas don issue 2 white black gold', 10000)
sneaker2 = Sneaker('adidas nmd r1 star wars the mandalorian', 14000)
sneaker3 = Sneaker('adidas top ten hi star wars the mandalorian the child', 9000)
db.session.add(sneaker1)
db.session.add(sneaker2)
db.session.add(sneaker3)

# insert user data
user1 = User('patkennedy79@gmail.com', 'password1234')
user2 = User('kennedyfamilyrecipes@gmail.com', 'PaSsWoRd')
user3 = User('blaa@blaa.com', 'MyFavPassword')
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()
