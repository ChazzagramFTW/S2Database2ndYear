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
                                party varchar(25) NOT NULL,
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
        
        cur.execute("SELECT name FROM parties WHERE id = " + str(x))
        party_name = cur.fetchone()

        # This result is then divided into a percentage of popular votes and placed into the results table.
        cur.execute("INSERT INTO results VALUES ('First Past The Post', ?, 0, 0.0, " + str(round((party_votes[0]/votes[0])*100, 2)) + ", 0.0)", (party_name))

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
        cur.execute("SELECT name FROM parties WHERE id = " + constituencyWinner[0]) # constituencyWinner[0]
        winnerName = cur.fetchone()

        # Retreives how many seats the party currently has.
        cur.execute("SELECT seats FROM results WHERE party = '" + winnerName[0] + "'")
        seatsandvotes = cur.fetchone()

        # And then increments the seats by one, and updating the results table.
        # The code also calculates the percentage of seats using the max amount of seats available.
        cur.execute("UPDATE results SET seats = " + str((seatsandvotes[0])+1) + ", seats_percent = " + str(round(((seatsandvotes[0]+1)/650)*100, 2)) + " WHERE party = '" + winnerName[0] + "'")

    # Fetches each party, its seats percent, and its vote percent.
    cur.execute("SELECT party, seats_percent, pop_votes_percent FROM results")
    results_percents = cur.fetchall()

    # Loops through each party in the results table.
    for row in results_percents:
        # And calculates the difference between the percentages, updating the tables 'difference' column.
        cur.execute("UPDATE results SET difference = ? WHERE party = ?", (str(round(row[2]-row[1], 2)), row[0]))





    # PR Pure

    # Loops through all 71 parties.
    for x in range(1,72):
        # For each party, the code grabs the total amount of votes they received as a party.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + str(x))
        party_votes = cur.fetchone()
        
        cur.execute("SELECT name FROM parties WHERE id = " + str(x))
        party_name = cur.fetchone()

        # This result is then divided into a percentage of popular votes and placed into the results table.
        cur.execute("INSERT INTO results VALUES ('Proportional Representation without modification', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round((party_votes[0]/votes[0])*650)), str(round((party_votes[0]/votes[0])*100, 2)), str(round((party_votes[0]/votes[0])*100, 2))))
    



    # PR 5%
    threshold_votes = 0
    # Loops through all 71 parties.
    for x in range(1,72):
        # For each party, the code grabs the total amount of votes they received as a party.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + str(x))
        party_votes = cur.fetchone()
    
        if(party_votes[0] >= (votes[0]*0.05)):
            threshold_votes = threshold_votes + party_votes[0]


    for x in range(1,72):
            # For each party, the code grabs the total amount of votes they received as a party.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + str(x))
            party_votes = cur.fetchone()
            
            cur.execute("SELECT name FROM parties WHERE id = " + str(x))
            party_name = cur.fetchone()

            if(party_votes[0] >= (votes[0]*0.05)):
                # This result is then divided into a percentage of popular votes and placed into the results table.
                cur.execute("INSERT INTO results VALUES ('Proportional Representation (5%)', ?, ?, ?, ?, ?)", (str(party_name[0]), str(round((party_votes[0]/threshold_votes)*650)), str(round((party_votes[0]/threshold_votes)*100, 2)), str(round((party_votes[0]/votes[0])*100, 2)), round(((party_votes[0]/votes[0])*100)-((party_votes[0]/threshold_votes)*100), 2)))

            else:
                cur.execute("INSERT INTO results VALUES ('Proportional Representation (5%)', ?, 0, 0, ?, ?)", (str(party_name[0]), str(round((party_votes[0]/votes[0])*100, 2)),str(round(0-(party_votes[0]/votes[0])*100, 2))))






    # PR (by County)

     # Loops through all 71 parties.
    for x in range(1,72):
        party_vote_percent = 0
        party_vote_count = 0
        for y in range(1,56):
            # For each party, the code grabs the total amount of votes they received as a party.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE county_id = " + str(y) + " AND party_id = " + str(x))
            party_votes = cur.fetchone()

            if party_votes[0] == None:
                if y == 55:
                    # This result is then divided into a percentage of popular votes and placed into the results table.
                    cur.execute("INSERT INTO results VALUES ('Proportional Representation (by County)', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round(650*(party_vote_percent/100))), str(round((party_vote_count/votes[0])*100, 2)), str(round(party_vote_percent, 2))))
                continue
            
            else:
                cur.execute("SELECT SUM(votes) FROM candidates WHERE county_id = " + str(y))
                county_votes = cur.fetchone()
                
                cur.execute("SELECT name FROM parties WHERE id = " + str(x))
                party_name = cur.fetchone()

                party_vote_count = party_vote_count + party_votes[0]

                party_vote_percent = party_vote_percent + (((party_votes[0]/county_votes[0])*100)/55)

                if(y == 55):
                    # This result is then divided into a percentage of popular votes and placed into the results table.
                    cur.execute("INSERT INTO results VALUES ('Proportional Representation (by County)', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round(650*(party_vote_percent/100))), str(round((party_votes[0]/votes[0])*100, 2)), str(round(party_vote_percent, 2))))





    # PR (by Region)

     # Loops through all 71 parties.
    for x in range(1,72):
        party_vote_percent = 0
        party_vote_count = 0
        for y in range(1,13):
            # For each party, the code grabs the total amount of votes they received as a party.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE region_id = " + str(y) + " AND party_id = " + str(x))
            party_votes = cur.fetchone()

            if party_votes[0] == None:
                if y == 12:
                    # This result is then divided into a percentage of popular votes and placed into the results table.
                    cur.execute("INSERT INTO results VALUES ('Proportional Representation (by Region)', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round(650*(party_vote_percent/100))), str(round((party_vote_count/votes[0])*100, 2)), str(round(party_vote_percent, 2))))
                continue
            
            else:
                cur.execute("SELECT SUM(votes) FROM candidates WHERE region_id = " + str(y))
                region_votes = cur.fetchone()
                
                cur.execute("SELECT name FROM parties WHERE id = " + str(x))
                party_name = cur.fetchone()

                party_vote_count = party_vote_count + party_votes[0]

                party_vote_percent = party_vote_percent + (((party_votes[0]/region_votes[0])*100)/12)

                if(y == 12):
                    # This result is then divided into a percentage of popular votes and placed into the results table.
                    cur.execute("INSERT INTO results VALUES ('Proportional Representation (by Region)', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round(650*(party_vote_percent/100))), str(round((party_votes[0]/votes[0])*100, 2)), str(round(party_vote_percent, 2))))






    # PR (by Country)

     # Loops through all 71 parties.
    for x in range(1,72):
        party_vote_percent = 0
        party_vote_count = 0
        for y in range(1,5):
            # For each party, the code grabs the total amount of votes they received as a party.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE country_id = " + str(y) + " AND party_id = " + str(x))
            party_votes = cur.fetchone()

            if party_votes[0] == None:
                if y == 4:
                    # This result is then divided into a percentage of popular votes and placed into the results table.
                    cur.execute("INSERT INTO results VALUES ('Proportional Representation (by Country)', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round(650*(party_vote_percent/100))), str(round((party_vote_count/votes[0])*100, 2)), str(round(party_vote_percent, 2))))
                continue
            
            else:
                cur.execute("SELECT SUM(votes) FROM candidates WHERE country_id = " + str(y))
                country_votes = cur.fetchone()
                
                cur.execute("SELECT name FROM parties WHERE id = " + str(x))
                party_name = cur.fetchone()

                party_vote_count = party_vote_count + party_votes[0]

                party_vote_percent = party_vote_percent + (((party_votes[0]/country_votes[0])*100)/4)

                if(y == 4):
                    # This result is then divided into a percentage of popular votes and placed into the results table.
                    cur.execute("INSERT INTO results VALUES ('Proportional Representation (by Country)', ?, ?, ?, ?, 0.0)", (str(party_name[0]), str(round(650*(party_vote_percent/100))), str(round((party_votes[0]/votes[0])*100, 2)), str(round(party_vote_percent, 2))))


    # Orders the results by most votes!
    cur.execute("SELECT * FROM results")
    rows = cur.fetchall()

    # Debugging Print
    for row in rows:
        print(row)

    #closes connection
    conn.close()

if __name__ == '__main__':
    main()
