#testing sending a postgres insert using psycopg across IP

import psycopg2
import sys, os
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import datetime
from datetime import datetime, date, timedelta, time
import os, sys, stat

PGHOST="127.0.0.1" #local
PGDATABASE="whateverTestDB"
PGUSER="postgres"
PGPASSWORD="whateverTestPass"

## ****** LOAD PSQL DATABASE ***** ##


# Set up a connection to the postgres server.
conn_string = "host="+ PGHOST +" port="+ "5432" +" dbname="+ PGDATABASE +" user=" + PGUSER +" password="+ PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cur = conn.cursor()

table = "test"
UniqueID = 1001
Home = "xxx"
Device = "AMG88xx_Grid_Eye"
Location = "Bedroom"
TimeStamp = datetime.utcnow()
list = "[21.75, 20.75, 21.5, 21.75, 21.5, 21.5, 21.75, 21.75][20.25, 21.25, 21.5, 21.25, 22.0, 21.5, 21.75, 21.5][21.5, 21.0, 21.5, 21.25, 21.5, 21.25, 21.25, 21.0][21.0, 21.25, 21.25, 21.5, 21.5, 21]"

cur.execute("INSERT INTO DBtablename (id, homeid, device_reporting, device_location, time_stamp, data) VALUES (%s, %s, %s, %s, %s, %s)",(UniqueID, Home, Device, Location, TimeStamp, list))

conn.commit()
cur.close()
conn.close()

