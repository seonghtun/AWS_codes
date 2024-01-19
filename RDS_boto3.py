import pymysql
import psycopg2
import sys
import boto3
import os

def mysql_conn():
    ENDPOINT="mysqldb.123456789012.us-east-1.rds.amazonaws.com"
    PORT="3306"
    USER="jane_doe"
    REGION="us-east-1"
    DBNAME="mydb"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

    #gets the credentials from .aws/credentials
    session = boto3.Session(profile_name='default')
    client = session.client('rds')

    token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

    try:
        conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e)) 

def postgresql_conn():
    ENDPOINT="postgresmydb.123456789012.us-east-1.rds.amazonaws.com"
    PORT="5432"
    USER="jane_doe"
    REGION="us-east-1"
    DBNAME="mydb"

    #gets the credentials from .aws/credentials
    session = boto3.Session(profile_name='RDSCreds')
    client = session.client('rds')

    token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token, sslrootcert="SSLCERTIFICATE")
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))
