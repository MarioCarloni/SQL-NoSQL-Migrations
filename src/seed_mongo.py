from mongoengine import connect, Document, IntField, StringField, disconnect
import pandas as pd
import os

if __name__ == "__main__":

  print('connect to mongo container, instantiate user class, and read user csv')

  connect(host = 'mongo_db', port = 27017)

  class User(Document):
    user_id =  IntField()
    user_firstname = StringField()
    user_lastname = StringField()
    user_email = StringField()

  df = pd.read_csv("import/users.csv") 

  try:

    print('create user record for each csv row, save to database')
    for index, row in df.iterrows():
      node = User(user_id = index)
      node.user_firstname = row.user_firstname
      node.user_lastname = row.user_lastname
      node.user_email = row.user_email
      node.save()

  except:

    print('something went wrong, deleting rows and disconnecting server')
    User.delete()
    disconnect()

  finally:
    
    print('translate mongoengine orm objects into pandas dataframe, print result')
    pdArray = []
    index = 0
    for row in User.objects:
      pdRow = {
        'user_id': index,
        'user_firstname': row.user_firstname,
        'user_lastname': row.user_lastname,
        'user_email': row.user_email
      }
      pdArray.append(pdRow)
      index+=1
    
    dfResult = pd.DataFrame(pdArray)

    print(dfResult)