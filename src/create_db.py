from app import db

# Drop all of the existing database tables
print("db.drop_all()")
db.drop_all()

# Create the database and the database table
print("db.create_all()")
db.create_all()
