import sqlite3
import subprocess

conn = sqlite3.connect('contacts.db')

def sql_fetch(con):

    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM people ORDER BY name')
    rows = cursorObj.fetchall()
    for row in rows:
      print(row)

def sql_add(name, number, email):
  cursor = conn.cursor()
  cursor.execute("SELECT rowid FROM people WHERE name = ?", (name,))
  data = cursor.fetchall()
  if len(data)==0:
    cur = conn.cursor()
    try:
      cur.execute(''' INSERT INTO people (name, number, email) VALUES (?,?,?)''',
         (name, number, email,))
      conn.commit()
    except sqlite3.IntegrityError as e:
      print('sqlite error: ', e.args[0])
  else:
    print("Contact already exists with that name")

def sql_del(name):
  sql = 'DELETE FROM people WHERE name =?'
  cur = conn.cursor()
  cur.execute(sql, (name,))
  conn.commit()

def sql_update_number(name, number):
  sql = "UPDATE people set number = ? where name = ?"
  cursor = conn.cursor()
  cursor.execute(sql, (number, name,))
  conn.commit()

def sql_update_email(name, email):
  sql = "UPDATE people set email = ? where name = ?"
  cursor = conn.cursor()
  cursor.execute(sql, (email, name,))
  conn.commit()

print("Command Line Contacts List")
cur = conn.cursor()
#cur.execute("create table people(name text, number text, email text)")
#t = ('aaa',)
#cur.execute('SELECT * FROM people WHERE name=?', t)

while(True):
  print("Please enter a Letter: A(Add Contact) D(Delete Contact) L(List Contacts) U(Update Contact) E(Exit)")
  var = input("Enter: ")
  print("You entered: " + var)
  subprocess.run(["clear"])
  if(var == 'E'):
    break
  elif(var == 'L'):
    sql_fetch(conn)
  elif(var == 'A'):
    name = input("Enter name: ")
    number = input("Enter number: ")
    email = input("Enter email: ")
    sql_add(name, number, email)
  elif(var == 'D'):
    print("Enter name of contact to delete: Action cannot be undone")
    deleteName = input("Enter: ")
    sql_del(deleteName)
  elif(var == 'U'):
    print("Enter name of contact to update")
    name = input("Enter name: ")
    print("Enter 1 to update number, 2 to update email")
    num = input("Enter: ")
    if(num == "1"):
      number = input("Enter number to update: ")
      sql_update_number(name, number)
    elif(num == "2"):
      email = input("Enter email to update: ")
      sql_update_email(name, email)


conn.close()
