from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 定义数据库连接
engine = create_engine('sqlite:///demo.db', echo=True)
Base = declarative_base()

# 定义一个示例模型（表）
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    pass

def create_table():
    pass

def insert_user(name, age):
    new_user = User(name=name, age=age)
    session.add(new_user)
    session.commit()

def update_user(user_id, new_age):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.age = new_age
        session.commit()

def query_users():
    users = session.query(User).all()
    return users

def delete_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()

def main():
    print('插入数据...')
    insert_user('Alice', 23)
    insert_user('Bob', 30)

    print('查询数据:')
    users = query_users()
    for user in users:
        print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')

    print('更新 Bob 的年龄...')
    # 假设 Bob 的 id 是 2
    update_user(2, 35)

    print('查询数据:')
    users = query_users()
    for user in users:
        print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')

    print('删除 Alice...')
    # 假设 Alice 的 id 是 1
    delete_user(1)

    print('最终数据:')
    users = query_users()
    for user in users:
        print(f'ID: {user.id}, Name: {user.name}, Age: {user.age}')

if __name__ == '__main__':
    main()
