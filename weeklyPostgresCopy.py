## Author: Leah Zulas, April 2019
## This program provides data scientists with a new weekly csv
## It connects to the postgres server residing on the same machine
## It copies one weeks worth of data to a location accessible by all parties. 
## Then it changes permissions so that the group dbusers can access it. 
## This is run via a CRON job on the server, each week at 4:01am UTC


import psycopg2
import sys, os
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import datetime
from datetime import datetime, date, timedelta, time
import os, sys, stat

PGHOST="127.0.0.1" #local host
PGDATABASE="testDatabase"
PGUSER="postgres"
PGPASSWORD="whateverPassword"

## ****** LOAD PSQL DATABASE ***** ##


# Set up a connection to the postgres server.
conn_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER +" password="+ PGPASSW$
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cur = conn.cursor()

#Test to make sure the connection works, not strictly speaking necessary
def load_data(schema, table):

    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)


#load_data("public", "events")

#What is now? When was last Sunday? Return these dates
def times_found():

    #When is now?
    now = datetime.utcnow()

    #Math requires pythons version of "today", to get last weeks "day" and then create a time stamp of now but la$
    today = date.today()
    last_week_day = today - timedelta(7)
    last_week = datetime.combine(last_week_day, datetime.now().time())

    #dates need to become strings and then delete the T that is int hat date for some reason
    now = datetime.isoformat(now)
    last_week = datetime.isoformat(last_week)
    now = now[0:10] + " " + now[11:]
    last_week = last_week[0:10] + " " + last_week[11:]

    #Print for verification before returning
    print(now)
    print(last_week)
    return (now, last_week)

def make_weekly_copy(fileLocation, table):

    #Open file into STDOUT for writing to
    f = open(fileLocation, 'w')
    #Get the times of this week and last week
    (now, last_week) = times_found()

    #PostgreSQL copy request
    sql_command = "COPY (SELECT * FROM " + table + " WHERE time_fired >= '" + last_week + "' AND time_fired < '" $
    #Print command for verification
    print(sql_command)
    #Run the above command using copy_expert
    cursor.copy_expert(sql_command, f)

    #close connection
    conn.commit()
    conn.close()

    # Assuming file exists, Set a file execute by the group. That way everyone can grab it off the server
    os.chmod(fileLocation, stat.S_IRWXG)

    # Set a file write by others.
#    os.chmod(fileLocation, stat.S_IWOTH)
    print("Changed mode successfully!!")

make_weekly_copy("/tmp/events.csv", "events")


