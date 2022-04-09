from cgitb import reset
from tabnanny import check
from unittest import result
import mysql.connector
from datetime import datetime
import json

# Connect to DB if database is specified, otherwise it creates the DB.
try: 
    mydb = mysql.connector.connect(
    host="localhost",
    user="simo",
    password="Password123!",
    database="collector"
    )
except:
    print("Error, trying second configuration")
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="newpassbubi10",
    database="mydatabase"
    )

mycursor = mydb.cursor(dictionary=True)

# Create DB
# mycursor.execute("CREATE DATABASE collector")

# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#   print(x)


# Add column
# mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

def create_tables():
    mycursor.execute("CREATE TABLE IF NOT EXISTS Customer (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), logo_path VARCHAR(10000))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Incident (id INT AUTO_INCREMENT PRIMARY KEY, customerId INT, date DATE, type VARCHAR(10000), FOREIGN KEY(customerId) REFERENCES Customer(id) ON DELETE CASCADE)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Evidence (id INT AUTO_INCREMENT PRIMARY KEY, incidentId INT NOT NULL, datetime DATETIME, killchain VARCHAR(255), host VARCHAR(255), host_type VARCHAR(255), image_path VARCHAR(10000), description TEXT NOT NULL, FOREIGN KEY(incidentId) REFERENCES Incident(id) ON DELETE CASCADE)")

def drop_tables(tables):
    for table in tables:
        sql = "DROP TABLE IF EXISTS %s" % table
        mycursor.execute(sql)
        mydb.commit()

def check_exist(table, attributes, values):
    sql = "SELECT * FROM %s WHERE" % table
    for i in range(0, len(attributes)):
        sql += " %s = '%s'" % (attributes[i], values[i])
        if i < len(attributes) -1:
            sql += " AND "
    
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if len(myresult) > 0:
        return True
    else:
        return False

def check_exist_table(table):
    sql = "SHOW TABLES"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    for t in myresult:
        if t[0] == str(table).lower():
            return True
    return False

def check_exist_column(table, column):
    sql = "SHOW COLUMNS FROM `%s`" % table
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for col in myresult:
        if col['Field'] == column:
            return True
    return False

# Creates a customer
def create_customer(name, logo_path):
    if check_exist("Customer", ["name"], [name]) == True:
        return -1
    else:
        sql = "INSERT INTO Customer (name, logo_path) VALUES (%s, %s)"
        mycursor.execute(sql, [name, logo_path])
        mydb.commit()
        return 0

#Removes a customer
def delete_customer(customerId):
    if check_exist("Customer", ["id"], [customerId]) == False:
        return -1
    else:
        sql = "DELETE FROM Customer WHERE id = '%s'" % customerId
        mycursor.execute(sql)
        mydb.commit()
        return 0

# Updates customer details
def update_customer(customerId, attributes, values):
    if check_exist("Customer", ["id"], [customerId]) == False:
        return -1
    if len(attributes) != len(values):
        return -2
    
    for a in attributes:
        if check_exist_column("Customer", a) == False:
            return -3

    sql = "UPDATE Customer SET "
    for i in range(len(attributes)):
        if i < len(attributes) -1:
            sql += "{} = %s, ".format(attributes[i])
        else:
            sql += "{} = %s ".format(attributes[i])
    sql += "WHERE id = %s" % customerId
    mycursor.execute(sql, values)
    mydb.commit()
    return 0

# Returns all the customers
def get_customers():
    sql = "SELECT * FROM `Customer`"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    return rows

# Creates an incident
def create_incident(customerId, date, type):
    if check_exist("Customer", ["id"], [customerId]) == False:
        return -1
    elif check_exist("Incident", ["customerId", "date", "type"], [customerId, date, type]) == True:
        return -2
    else:
        sql = "INSERT INTO Incident (customerId, date, type) VALUES (%s, '%s', '%s')" % (customerId, date, type)
        mycursor.execute(sql)
        mydb.commit()
        return 0

# Deletes an incident
def delete_incident(incidentId):
    if check_exist("Incident", ["id"], [incidentId]) == False:
        return -1
    sql = "DELETE FROM Incident WHERE id = '%s'" % incidentId
    mycursor.execute(sql)
    mydb.commit()
    return 0


# Returns all the incidents
def get_incidents():
    sql = "SELECT * FROM Incident"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# Returns all the incidents of a customer
def get_customer_incidents(customerId):
    sql = "SELECT * FROM Incident WHERE customerId = '%s'" % (customerId)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

# Creates a new evidence
def create_evidence(incidentId, datetime, killchain, host, host_type, image_path, description):
    sql = "INSERT INTO Evidence (incidentId, datetime, killchain, host, host_type, image_path, description) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, [incidentId, datetime, killchain, host, host_type, image_path, description])
    mydb.commit()
    return 0

# Deletes an evidence
def delete_evidence(evidenceId):
    if check_exist("Evidence", ["id"], [evidenceId]) == False:
        return -1
    sql = "DELETE FROM Evidence WHERE id = '%s'" % evidenceId
    mycursor.execute(sql)
    mydb.commit()
    return 0

# Updates an evidence
def update_evidence(evidenceId, attributes, values):
    if check_exist("Evidence", ["id"], [evidenceId]) == False:
        return -1
    if len(attributes) != len(values):
        return -2
    
    for a in attributes:
        if check_exist_column("Evidence", a) == False:
            return -3

    sql = "UPDATE Evidence SET "
    for i in range(len(attributes)):
        if i < len(attributes) -1:
            sql += "{} = %s, ".format(attributes[i])
        else:
            sql += "{} = %s ".format(attributes[i])
    sql += "WHERE id = %s" % evidenceId
    mycursor.execute(sql, values)
    mydb.commit()
    return 0

# Returns the evidences of an incident
def get_incident_evidences(incidentId):
    if check_exist("Incident", ["id"], [incidentId]) == False:
        return -1
    sql = "SELECT * FROM Evidence WHERE incidentId = '%s'" % (incidentId)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


# Returns customerId from incidentId
def get_customerId_from_incidentId(incidentId):
    if check_exist("Incident", ["id"], [incidentId]) == False:
        return -1
    sql = "SELECT customerId FROM Incident WHERE id = '%s'" % (incidentId)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult[0]["customerId"]

def get_customer_name_from_id(customerId):
    if check_exist("Customer", ["id"], [customerId]) == False:
        return -1
    sql = "SELECT name FROM Customer WHERE id = '%s'" % (customerId)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult[0]["name"]
