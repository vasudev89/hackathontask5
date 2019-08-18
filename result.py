from tabulate import tabulate
import pymysql, datetime

dbConn = pymysql.connect("remotemysql.com","TVyfBaNPgM","0AlfWH2RNS","TVyfBaNPgM")

def validate(date_text):
  try:
    datetime.datetime.strptime(date_text, '%m/%d/%Y')
    return True
  except ValueError as e:
    print( e )
    return False

def addRecord(): 
  
  data = []
  data.append( input("ENTER NAME(max 25 chars):") )
  data.append( input("ENTER EVENT DETAILS(max 50 chars):") )
  data.append( input("ENTER DATE(mm/dd/yyyy):") )
  data.append( input("ENTER DATE(mm/dd/yyyy):") )

  if data[0] == "": print("INVALID NAME"); return;
  if data[1] == "": print("INVALID EVENT DETAILS"); return;
  if not validate(data[2]): print("INVALID DATE"); return;

  query = "INSERT INTO scheduler (NAME, EVENTDETAILS, DATE) VALUES ('%s','%s','%s')" % (data[0][:25],data[1][:50],data[2])
  cursor = dbConn.cursor()
  cursor.execute(query)
  cursor.close()
  dbConn.commit()
  print( "RECORD ADDED SUCCESSFULLY" )
  
def viewRecords():

  query = "select * from scheduler"
  cursor = dbConn.cursor(pymysql.cursors.DictCursor)
  cursor.execute(query)

  res = list( cursor.fetchall() )
  # print( res )
  
  if len(res) != 0:
    print("RESULT: ")
    print()
    print( tabulate( res , headers="keys" , tablefmt="grid" ) )
    print( "#" * 100 )
  else:
    print("RESULT: NO RECORDS EXIST")
    print()
    print( "#" * 100 )
  
  cursor.close()
  
def viewRecordsForSingleUser(): 
  
  username = input("ENTER USERNAME: ")

  query = "select * from scheduler where NAME = '%s'" % username
  cursor = dbConn.cursor(pymysql.cursors.DictCursor)
  cursor.execute(query)

  res = list( cursor.fetchall() )
  # print( res )
  
  if len(res) != 0:
    print("RESULT: ")
    print()
    print( tabulate( res , headers="keys" , tablefmt="grid" ) )
    print( "#" * 100 )
  else:
    print("RESULT: NO RECORDS EXIST")
    print()
    print( "#" * 100 )
  
  cursor.close()

def deleteAllRecords():
  query = "DELETE FROM scheduler"
  cursor = dbConn.cursor()
  cursor.execute(query)
  cursor.close()
  dbConn.commit()
  print("ALL RECORDS DELETED SUCCESSFULLY")

def deleteAllRecordsForUser():

  username = input("ENTER USERNAME: ")

  query = "DELETE FROM scheduler where NAME LIKE '%s'" % username
  cursor = dbConn.cursor()
  cursor.execute(query)
  cursor.close()
  dbConn.commit()
  print("ALL RECORDS FOR %s DELETED SUCCESSFULLY" % username) 

menu = {
  1: addRecord,
  2: viewRecords,
  3: viewRecordsForSingleUser,
  4: deleteAllRecords,
  5: deleteAllRecordsForUser,
}

while True:

  print()
  print( "1. Add An Event" )
  print( "2. View All Events" )
  print( "3. View All Events for a User" )
  print( "4. Delete all Events" )
  print( "5. Delete all Events for a User" )
  print( "6. Exit" )
  c = int( input("ENTER CHOICE:") )

  print()

  if c == 6: break
  elif c not in menu: print( "INVALID CHOICE" )
  else:
    menu[c]()