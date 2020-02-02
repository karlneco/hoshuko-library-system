from hls import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

########################################################################### User
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))


    def __init__(self,email,password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.email

######################################################################### Patron
# Patrons borrow materials from the library
class Patron(db.Model):
    __tablename__ = 'patron'

    id = db.Column(db.Integer,primary_key=True)
    patron_number = db.Column(db.Text)
    name = db.Column(db.Text)
    furigana = db.Column(db.Text)
    gender = db.Column(db.Text)
    contact = db.Column(db.Text)
    patron_type_id =  db.Column(db.Integer, db.ForeignKey('patron_type.id'))
    patron_type = db.relationship("PatronType")


    def __init__(self, patron_number,name,furigana,gender,patron_type_id):
        self.patron_number = patron_number
        self.name = name
        self.furigana = furigana
        self.gender = gender
        self.patron_type_id = patron_type_id

    def __repr__(self):
        return f'Patron {self.name}({self.furigana}): {patron_type.description}'


##################################################################### PatronType
# Patrons have a type
class PatronType(db.Model):
    __tablename__ = 'patron_type'

    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.Text)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f'{self.description}'


########################################################################### Item
# Items are things that patrons can borrow
#  Items have a Type
#  Items have Authors
#  Items have a Publisher
#  Items have a Field
class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer,primary_key=True)
    item_number = db.Column(db.Text)
    title = db.Column(db.Text)
    add_date = db.Column(db.Date)
    purchase_price = db.Column(db.Numeric)
    note = db.Column(db.Text)


    item_type_id =  db.Column(db.Integer, db.ForeignKey('item_type.id'))
    type = db.relationship("ItemType")

    author_id =  db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author")

    publisher_id =  db.Column(db.Integer, db.ForeignKey('publisher.id'))
    publisher = db.relationship("Publisher")

    field_id =  db.Column(db.Integer, db.ForeignKey('item_field.id'))
    field = db.relationship("ItemField")


    def __init__(self, item_number, title, add_date, purchase_price):
        self.item_number = item_number
        self.title = title
        self.add_date = add_date
        self.purchase_price = purchase_price


    def __repr__(self):
        return f'Item is a {type.description}: {self.title} by {author.name}, published by {publisher.name}'


####################################################################### ItemType
# Items are of a type
class ItemType(db.Model):
    __tablename__ = 'item_type'

    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.Text)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f'{self.description}'

######################################################################### Author
# Authors create books
class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

###################################################################### Publisher
# Publishers publish books
class Publisher(db.Model):
    __tablename__ = 'publisher'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

########################################################################## Field
# Books are in a field
class Field(db.Model):
    __tablename__ = 'item_field'

    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.Text)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f'{self.description}'



#################################################################### ItemHistory
# Patrons borrow Items
class ItemHistory(db.Model):
    __tablename__ = 'item_history'

    id = db.Column(db.Integer,primary_key=True)
    borrow_date = db.Column(db.Date)
    expected_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    patron_id = db.Column(db.Integer, db.ForeignKey('patron.id'))
    patron = db.relationship("Patron")

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship("Item")


    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f'{self.description}'



class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    date = db.Column(db.Text)
    grade = db.Column(db.Integer)
    comments = db.Column(db.Text)

    # one-to-many; one lesson may have many materials
    lesson_materials = db.relationship('LessonMaterial', backref='lesson_material', lazy='dynamic')

    def __init__(self, name, grade):
        self.name=name
        self.grade=grade


    def __repr__(self):
        return f'{self.name} is a grade {self.grade} lesson with {lesson_materials.length}'

class MaterialType(db.Model):
    __tablename__ = 'material_type'
    code = db.Column(db.Text,primary_key=True)
    name = db.Column(db.Text)
    instructions = db.Column(db.Text)
    custom_template = db.Column(db.Boolean)

    def __init__(self,code,name,insturctions):
        self.code=code
        self.name=name
        self.instructions=insturctions

    def __repr__(self):
        return f'{self.name} is a material identified by code {self.code}'

class LessonMaterial(db.Model):
    __tablename__ = 'lesson_material'
    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.Text) # this can indicate the worksheet name and number
    content = db.Column(db.Text)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    material_code = db.Column(db.Text, db.ForeignKey('material_type.code'))
    material = db.relationship("MaterialType")



    def __init__(self,name,content,lesson_id,material_code):
        self.name=name
        self.content=content
        self.lesson_id = lesson_id
        self.material_code = material_code

    def __repr__(self):
        return f'this is the worksheet {self.name} for the lesson'
