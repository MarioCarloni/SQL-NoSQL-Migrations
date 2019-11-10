from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Date
import pandas as pd
import os

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  user_id = Column(Integer, primary_key=True)
  user_firstname = Column(String)
  user_lastname = Column(String)
  user_email = Column(String)


if __name__ == "__main__":

  user = os.environ['db_user']
  pw = os.environ['db_pw']
  dbName = os.environ['db_name']

  print('create postgres session with environment params')
  engine = create_engine('postgresql://' + user + ':' + pw + '@postgres_db/' + dbName)
  Session = sessionmaker(bind=engine)
  Session.configure(bind=engine)
  s = Session()

  try:

    print('create users schema, read user data from csv')
    Base.metadata.create_all(engine)
    file_name = "import/users.csv"
    df=pd.read_csv(file_name) 

    print('append each csv row as users table record from orm')
    for index, row in df.iterrows():
      record = User(**{
        'user_firstname' : row.user_firstname,
        'user_lastname' : row.user_lastname,
        'user_email' : row.user_email
      })
      s.add(record) 
    
    print('commit transaction')
    s.commit() 

  except:

    print('on error, roll back transaction')
    s.rollback() 
    s.close()
    
  finally:

    print('parse orm query results into pandas dataframe, print dataframe, then close connection')
    orm_statement = s.query(User).order_by(User.user_id).statement
    df = pd.read_sql(orm_statement,s.bind)
    print(df)
    s.close()