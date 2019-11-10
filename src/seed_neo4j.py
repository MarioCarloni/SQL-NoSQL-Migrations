from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property
import pandas as pd
import os

class User(GraphObject):
  __primarykey__ = "user_id"

  user_id = Property()
  user_firstname = Property()
  user_lastname = Property()
  user_email = Property()

if __name__ == "__main__":

  print('connecting to neo4j')
  graph = Graph(host = "neo4j_db", user = "neo4j", password = os.environ['db_pw'])
  
  print('reading csv')
  df = pd.read_csv("import/users.csv") 

  print('begin transaction')
  tx = graph.begin()

  try:

    print('create nodes for each csv row')
    for index, row in df.iterrows():
      node = User()
      node.user_id = index
      node.user_firstname = row.user_firstname
      node.user_lastname = row.user_lastname
      node.user_email = row.user_email
      graph.push(node)

    print('commit transaction')
    tx.commit()
    tx.finished()
  except:

    print('errpr, rolling back')
    tx.rollback()
    tx.finished()
  finally:
    
    print('query user nodes')
    userMatch = User.match(graph)

    print('initialize dataframe')
    pdArray = []

    print('append user node values as new dataframe rows')
    index = 0
    for row in userMatch:
      pdRow = {
        'user_id': index,
        'user_firstname': row.user_firstname,
        'user_lastname': row.user_lastname,
        'user_email': row.user_email
      }
      pdArray.append(pdRow)
      index+=1

    resultDF = pd.DataFrame(pdArray)

    print(resultDF)
