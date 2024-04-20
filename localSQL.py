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
    database = r"C:\Users\charl\Documents\GitHub\S2Database2ndYear\data\pythonsqlite.db"
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
    
    with open('data\ConstituencyCSV.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO constituencies VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS counties (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\CountyCSV.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO counties VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS regions (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\RegionCSV.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO regions VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS countries (
                                        id PRIMARY KEY
                                    ); """)
    
    with open('data\CountryCSV.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO countries VALUES (?)', list(csv_reader))
    
    cur.execute(""" CREATE TABLE IF NOT EXISTS parties (
                                        id varchar(5) PRIMARY KEY,
                                        name varchar(25) NOT NULL
                                    ); """)
    
    with open('data\PartyCSV.csv', 'r', encoding='utf-8-sig') as csv_file:
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
    

    with open('data\CandidatesCSV.csv', 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)

        cur.executemany('INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?)', list(csv_reader))

    cur.execute(""" CREATE TABLE IF NOT EXISTS results (
                                system varchar(25) NOT NULL,
                                party_id varchar(25) NOT NULL,
                                seats int NOT NULL,
                                seats_percent float NOT NULL,
                                pop_votes_percent float NOT NULL,
                                difference float NOT NULL
                            ); """)
    
    cur.execute("SELECT SUM(votes) FROM candidates")
    votes = cur.fetchone()

    # Loops through all 71 parties.
    for x in range(1,72):
        # For each party, the code grabs the total amount of votes they received as a party.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + str(x))
        party_votes = cur.fetchone()
        # This result is then divided into a percentage of popular votes and placed into the results table.
        cur.execute("INSERT INTO results VALUES ('PR', '" + str(x) + "', 0, 0.0, " + str((party_votes[0]/votes[0])*100) + ", 0.0)")

    cur.execute("SELECT id FROM constituencies")


    #returns a list of results 
    rows = cur.fetchall()

    # Loops through all constituencies.
    for x in range (1,651):
        # Grab amount of votes from all candidates within the current constituency.
        cur.execute("SELECT votes FROM candidates WHERE constituency_id = " + str(x))
        candidatesrows = cur.fetchall()

        # Finds the party with the most amount of votes in that constituency.
        cur.execute("SELECT party_id FROM candidates WHERE votes = " + str(max(candidatesrows[0])))
        constituencyWinner = cur.fetchone()

        # Grabs the constituency ID from the parties table.
        cur.execute("SELECT * FROM parties WHERE id = " + constituencyWinner[0]) # constituencyWinner[0]
        print("Winning Party ID: " + constituencyWinner[0])
        winnerName = cur.fetchone()

        # Retreives how many seats the party currently has.
        cur.execute("SELECT seats FROM results WHERE party_id = " + winnerName[0])
        seatsandvotes = cur.fetchone()

        # And then increments the seats by one, and updating the results table.
        # The code also calculates the percentage of seats using the max amount of seats available.
        cur.execute("UPDATE results SET seats = " + str((seatsandvotes[0])+1) + ", seats_percent = " + str(((seatsandvotes[0]+1)/650)*100) + " WHERE party_id = " + winnerName[0])

    # Fetches each party, its seats percent, and its vote percent.
    cur.execute("SELECT party_id, seats_percent, pop_votes_percent FROM results")
    results_percents = cur.fetchall()

    # Loops through each party in the results table.
    for row in results_percents:
        # And calculates the difference between the percentages, updating the tables 'difference' column.
        cur.execute("UPDATE results SET difference = " + str(row[2]-row[1]) + " WHERE party_id = " + str(row[0]))

    # Orders the results by most votes!
    cur.execute("SELECT * FROM results ORDER BY seats DESC")
    rows = cur.fetchall()

    # Debugging Print
    for row in rows:
        print(row)
    
    #closes connection
    conn.close()

if __name__ == '__main__':
    main()
