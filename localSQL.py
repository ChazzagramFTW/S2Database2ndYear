import sqlite3
import csv
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def main():
    database = r"C:\Users\Charlie\Desktop\database\pythonsqlite.db"
    # create a database connection
    conn = create_connection(database)
    #create cursor to collect data from db
    cur = conn.cursor()
    #drops table project if exists
    cur.execute("DROP TABLE IF EXISTS candidates")
    #runs create table script

    cur.execute(""" CREATE TABLE IF NOT EXISTS constituencies (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\ConstituencyCSV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO constituencies VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS counties (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\CountyCSV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO counties VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS regions (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\RegionCSV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO regions VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS countries (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\CountryCSV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO countries VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS parties (
                                        id PRIMARY KEY,
                                        name varchar(25) NOT NULL
                                    ); """)
    
    with open('data\PartyCSV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO parties VALUES (?, ?)', list(csv_reader))

    cur.execute(""" CREATE TABLE IF NOT EXISTS candidates (
                                        id PRIMARY KEY,
                                        name varchar(25) NOT NULL,
                                        constituency_id varchar(5) NOT NULL,
                                        county_id varchar(5) NOT NULL,
                                        region_id varchar(5) NOT NULL,
                                        country_id varchar(5) NOT NULL,
                                        party_id varchar(5) NOT NULL,
                                        votes integer NOT NULL,
                                        FOREIGN KEY (constituency_id) REFERENCES constituencies(id),
                                        FOREIGN KEY (county_id) REFERENCES counties(id),
                                        FOREIGN KEY (region_id) REFERENCES regions(id),
                                        FOREIGN KEY (country_id) REFERENCES countries(id),
                                        FOREIGN KEY (party_id) REFERENCES parties(id)
                                    ); """)
    

    with open('data\CandidatesCSV.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?)', list(csv_reader))


    cur.execute("SELECT * FROM candidates")
    
    
    #returns a list of results 
    rows = cur.fetchall()
    
    #each row is a tuple of values
    for row in rows:
        print(row)
        #return index 0 and type
        print(type(row[0]), row[0])
        #return index 1 and type
        print(type(row[1]), row[1])

        print(type(row[2]), row[2])

        print(type(row[3]), row[3])

        print(type(row[4]), row[4])

        print(type(row[5]), row[5])

        print(type(row[6]), row[6])

        print(type(row[7]), row[7])


        cur.execute(""" CREATE TABLE IF NOT EXISTS results (
                                        system varchar(25) NOT NULL,
                                        party varchar(25) NOT NULL,
                                        seats int NOT NULL,
                                        seats_percent varchar(3) NOT NULL,
                                        pop_votes_percent varchar(3) NOT NULL,
                                        test varchar(3) NOT NULL,
                                        difference varchar(3) NOT NULL
                                    ); """)
    
    #closes connection
    conn.close()

if __name__ == '__main__':
    main()
