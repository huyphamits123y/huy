from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from gkwebs import db, app
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime

class UserRole(UserEnum):
    USER = 1
    ADMIN = 2

class BaseModel(db.Model):
    __abstract__  = True
    id = Column(Integer, primary_key=True,  autoincrement=True)

class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(20), nullable=False)
    product = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name

prod_tag = db.Table('prod_tag',
                    Column('product_id', ForeignKey('product.id'), nullable=False, primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))
class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float,  default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date= Column(DateTime, default=datetime.now())
    category_id= Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    def __str__(self):
        return  self.name


    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default = UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name

class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)
class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
if __name__=='__main__':
     with app.app_context():
        # db.create_all()

        import hashlib
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='Huy', username='huypham', password=password,
                 avatar='img_7.png',
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()
        c1 = Category(name='Thương gia')
        c2 = Category(name='Phổ thông')


        db.session.add_all([c1, c2])
        db.session.commit()
        p1 = Product(name='Thành Phố Hồ Chí Minh-Hà Nội', description='Khởi hành lúc 9h (20-12-2022)', price=25000000,
                     image='https://media.vietravel.com/images/news/ha-noi-1.jpg',
                     category_id=1)
        p2 = Product(name='Thành Phố Hồ Chí Minh-Đà Nẵng', description='Khởi hành lúc 12h (18-12-2022)', price=38000000,
                     image='http://divui.com/blog/wp-content/uploads/2018/10/111111.jpg',
                     category_id=1)
        p3 = Product(name='Thành Phố Hồ Chí Minh-Phú Quốc', description='Khởi hành lúc 8h (30-12-2022)', price=18000000,
                     image='https://statics.vntrip.vn/data-v2/data-guide/img_content/1470302454_anh-11.jpg',
                     category_id=1)
        p4 = Product(name='Thành Phố Hồ Chí Minh-Huế', description='Khởi hành lúc 1h (3-12-2022)', price=22000000,
                     image='https://huesmiletravel.com.vn/images/dai_noi_ve_dem.jpg',
                     category_id=2)
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()


