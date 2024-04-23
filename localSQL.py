import sqlite3
import csv
import math
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

            if party_votes[0] is None:
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

            if party_votes[0] is None:
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

            if party_votes[0] is None:
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







    # Largest Remainder (by County)

    # Overall seats as a dictionary, to hold the parties and their overall seat count for later insertation.
    overall_seats = {}
    cur.execute("SELECT id FROM parties")
    parties = cur.fetchall()

    # Adding each party to the dictionary.
    for row in parties:
        overall_seats[str(row[0])] = 0

    # Loop through each county.
    for x in range(1, 56):
        # Remainders dictionary to hold each remainder value for each parties seats.
        remainders = {}
        
        # Fetching current counties total vote count.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE county_id = " + str(x))
        county_votes = cur.fetchone()[0]

        # variable to hold remaining seats in the county.
        county_seats = 0

        # Loop through each constituency.
        for y in range(1, 651):
            # Grabs the constituency and county to check if the constituency comes up in that county.
            cur.execute("SELECT * FROM candidates WHERE county_id = " + str(x) + " AND constituency_id = " + str(y))
            constituency_in_county = cur.fetchall()
            if constituency_in_county:
                county_seats = county_seats + 1
        
        # Calculates this county's Hare Quota.
        county_hare_quota = county_votes / county_seats

        # Loop through each party.
        for y in range(1, 72):
            # Fetches the total votes the current party received in this county.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE county_id = " + str(x) + " AND party_id = " + str(y))
            party_votes = cur.fetchone()

            # If no votes, skip iteration.
            if party_votes[0] is None:
                continue
            
            # Calculates the parties seats for the current county.
            party_seats = party_votes[0] / county_hare_quota

            # Rounds the seats down to nearest whole number (Seats Awarded)
            floored_seats = math.floor(party_seats)

            # Adds the earnt seats to the party, and deducts the counties remaining seats by the amount.
            party_id_str = str(y)
            if party_id_str in overall_seats:
                overall_seats[party_id_str] = overall_seats[party_id_str] + floored_seats
                county_seats = county_seats - floored_seats

            # Grabs the remainder from the seats value, deducting the rounded down value from the real value.
            party_seats_remainder = party_seats - floored_seats
            remainders[party_id_str] = party_seats_remainder

        # Sorts the remainders in order highest to lowest, converting the dictionary to a list of tuples.
        remainders = sorted(remainders.items(), key=lambda x: x[0])

        # Loops through all party's remainders.
        for party_id, party_seats_remainder in remainders:
            # Checks if the county has ran out of seats before giving out more. (They can't be too kind! Like they have been..)
            if county_seats == 0:
                break

            # Adds seat to parties total seats, deducts a seat from the county's total seats.
            total_party_seats = overall_seats[party_id] + 1
            overall_seats[party_id] = total_party_seats
            county_seats = county_seats - 1

    # Loops through all parties in the overall seats dictionary, to grab the parties name via id, and insert their total seats.
    for party_id, seats in overall_seats.items():
        # Grabs party name.
        cur.execute("SELECT name FROM parties WHERE id = " + party_id)
        party_name = cur.fetchone()

        # Grabs party total votes.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + party_id)
        party_votes = cur.fetchone()

        # Inserting the values into the results table.
        cur.execute("INSERT INTO results VALUES ('Largest Remainder (by County)', ?, ?, ?, ?, ?)", (party_name[0], seats, round(((seats/650)*100), 2), round((party_votes[0]/votes[0])*100, 2), round(((party_votes[0]/votes[0])*100)-((seats/650)*100), 2)))







    # Largest Remainder (by Region)

    # Overall seats as a dictionary, to hold the parties and their overall seat count for later insertation.
    overall_seats = {}
    cur.execute("SELECT id FROM parties")
    parties = cur.fetchall()

    # Adding each party to the dictionary.
    for row in parties:
        overall_seats[str(row[0])] = 0

    # Loop through each region.
    for x in range(1, 13):
        # Remainders dictionary to hold each remainder value for each parties seats.
        remainders = {}
        
        # Fetching current counties total vote count.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE region_id = " + str(x))
        region_votes = cur.fetchone()[0]

        # variable to hold remaining seats in the region.
        region_seats = 0

        # Loop through each constituency.
        for y in range(1, 651):
            # Grabs the constituency and region to check if the constituency comes up in that region.
            cur.execute("SELECT * FROM candidates WHERE region_id = " + str(x) + " AND constituency_id = " + str(y))
            constituency_in_region = cur.fetchall()
            if constituency_in_region:
                region_seats = region_seats + 1
        
        # Calculates this region's Hare Quota.
        region_hare_quota = region_votes / region_seats

        # Loop through each party.
        for y in range(1, 72):
            # Fetches the total votes the current party received in this region.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE region_id = " + str(x) + " AND party_id = " + str(y))
            party_votes = cur.fetchone()

            # If no votes, skip iteration.
            if party_votes[0] is None:
                continue
            
            # Calculates the parties seats for the current region.
            party_seats = party_votes[0] / region_hare_quota

            # Rounds the seats down to nearest whole number (Seats Awarded)
            floored_seats = math.floor(party_seats)

            # Adds the earnt seats to the party, and deducts the counties remaining seats by the amount.
            party_id_str = str(y)
            if party_id_str in overall_seats:
                overall_seats[party_id_str] = overall_seats[party_id_str] + floored_seats
                region_seats = region_seats - floored_seats

            # Grabs the remainder from the seats value, deducting the rounded down value from the real value.
            party_seats_remainder = party_seats - floored_seats
            remainders[party_id_str] = party_seats_remainder

        # Sorts the remainders in order highest to lowest, converting the dictionary to a list of tuples.
        remainders = sorted(remainders.items(), key=lambda x: x[0])

        # Loops through all party's remainders.
        for party_id, party_seats_remainder in remainders:
            # Checks if the region has ran out of seats before giving out more. (They can't be too kind! Like they have been..)
            if region_seats == 0:
                break

            # Adds seat to parties total seats, deducts a seat from the region's total seats.
            total_party_seats = overall_seats[party_id] + 1
            overall_seats[party_id] = total_party_seats
            region_seats = region_seats - 1

    # Loops through all parties in the overall seats dictionary, to grab the parties name via id, and insert their total seats.
    for party_id, seats in overall_seats.items():
        # Grabs party name.
        cur.execute("SELECT name FROM parties WHERE id = " + party_id)
        party_name = cur.fetchone()

        # Grabs party total votes.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + party_id)
        party_votes = cur.fetchone()

        # Inserting the values into the results table.
        cur.execute("INSERT INTO results VALUES ('Largest Remainder (by Region)', ?, ?, ?, ?, ?)", (party_name[0], seats, round(((seats/650)*100), 2), round((party_votes[0]/votes[0])*100, 2), round(((party_votes[0]/votes[0])*100)-((seats/650)*100), 2)))








    # Largest Remainder (by Country)

    # Overall seats as a dictionary, to hold the parties and their overall seat count for later insertation.
    overall_seats = {}
    cur.execute("SELECT id FROM parties")
    parties = cur.fetchall()

    # Adding each party to the dictionary.
    for row in parties:
        overall_seats[str(row[0])] = 0

    # Loop through each country.
    for x in range(1, 5):
        # Remainders dictionary to hold each remainder value for each parties seats.
        remainders = {}
        
        # Fetching current counties total vote count.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE country_id = " + str(x))
        country_votes = cur.fetchone()[0]

        # variable to hold remaining seats in the country.
        country_seats = 0

        # Loop through each constituency.
        for y in range(1, 651):
            # Grabs the constituency and country to check if the constituency comes up in that country.
            cur.execute("SELECT * FROM candidates WHERE country_id = " + str(x) + " AND constituency_id = " + str(y))
            constituency_in_country = cur.fetchall()
            if constituency_in_country:
                country_seats = country_seats + 1
        
        # Calculates this country's Hare Quota.
        country_hare_quota = country_votes / country_seats

        # Loop through each party.
        for y in range(1, 72):
            # Fetches the total votes the current party received in this country.
            cur.execute("SELECT SUM(votes) FROM candidates WHERE country_id = " + str(x) + " AND party_id = " + str(y))
            party_votes = cur.fetchone()

            # If no votes, skip iteration.
            if party_votes[0] is None:
                continue
            
            # Calculates the parties seats for the current country.
            party_seats = party_votes[0] / country_hare_quota

            # Rounds the seats down to nearest whole number (Seats Awarded)
            floored_seats = math.floor(party_seats)

            # Adds the earnt seats to the party, and deducts the counties remaining seats by the amount.
            party_id_str = str(y)
            if party_id_str in overall_seats:
                overall_seats[party_id_str] = overall_seats[party_id_str] + floored_seats
                country_seats = country_seats - floored_seats

            # Grabs the remainder from the seats value, deducting the rounded down value from the real value.
            party_seats_remainder = party_seats - floored_seats
            remainders[party_id_str] = party_seats_remainder

        # Sorts the remainders in order highest to lowest, converting the dictionary to a list of tuples.
        remainders = sorted(remainders.items(), key=lambda x: x[0])

        # Loops through all party's remainders.
        for party_id, party_seats_remainder in remainders:
            # Checks if the country has ran out of seats before giving out more. (They can't be too kind! Like they have been..)
            if country_seats == 0:
                break

            # Adds seat to parties total seats, deducts a seat from the country's total seats.
            total_party_seats = overall_seats[party_id] + 1
            overall_seats[party_id] = total_party_seats
            country_seats = country_seats - 1

    # Loops through all parties in the overall seats dictionary, to grab the parties name via id, and insert their total seats.
    for party_id, seats in overall_seats.items():
        # Grabs party name.
        cur.execute("SELECT name FROM parties WHERE id = " + party_id)
        party_name = cur.fetchone()

        # Grabs party total votes.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + party_id)
        party_votes = cur.fetchone()

        # Inserting the values into the results table.
        cur.execute("INSERT INTO results VALUES ('Largest Remainder (by Country)', ?, ?, ?, ?, ?)", (party_name[0], seats, round(((seats/650)*100), 2), round((party_votes[0]/votes[0])*100, 2), round(((party_votes[0]/votes[0])*100)-((seats/650)*100), 2)))







    # D'Hont (by County)

    # Overall seats as a dictionary, to hold the parties and their overall seat count for later insertation.
    overall_seats = {}
    # Current seats dictionary to hold each parties current seats.
    current_seats = {}
    # Vote quotients dictionary to hold each parties vote quotient.
    vote_quotients = {}

    # Gets all parties id's from parties table.
    cur.execute("SELECT id FROM parties")
    parties = cur.fetchall()

    # Adding each party to the dictionary.
    for row in parties:
        overall_seats[str(row[0])] = 0

    # Loop through each county.
    for x in range(1, 56):

        # Adding each party to the current votes dictionary.
        for row in parties:
            current_seats[str(row[0])] = 0

        county_seats = 0
        # Loop through each constituency.
        for y in range(1, 651):
            # Grabs the constituency and county to check if the constituency comes up in that county.
            cur.execute("SELECT * FROM candidates WHERE county_id = " + str(x) + " AND constituency_id = " + str(y))
            constituency_in_county = cur.fetchall()

            # Adds to total "seats" in county if the constituency is in the county.
            if constituency_in_county:
                county_seats = county_seats + 1

        # Loops through all seats.
        for y in range(1,(county_seats+1)):
            sorted_vote_quotients = {}
        # Loop through each party.
            for z in range(1, 72):
                # Fetches the total votes the current party received in this county.
                cur.execute("SELECT SUM(votes) FROM candidates WHERE county_id = " + str(x) + " AND party_id = " + str(z))
                party_votes = cur.fetchone()

                # If no votes, skip iteration.
                if party_votes[0] is None:
                    # add party to vote quotients.
                    continue
                
                # Calculates the parties seats for the current county.
                vote_quotients[str(z)] = party_votes[0] / (current_seats[str(z)] + 1)

            # Sorts the vote quotients in order highest to lowest, converting the dictionary to a list of tuples.
            sorted_vote_quotients = sorted(vote_quotients.items(), key=lambda x: x[1], reverse=True)

            # Adds to parties current seats.
            current_seats[str(sorted_vote_quotients[0][0])] = current_seats[str(sorted_vote_quotients[0][0])] + 1

            # Adds to parties overall seats.
            overall_seats[str(sorted_vote_quotients[0][0])] = overall_seats[str(sorted_vote_quotients[0][0])] + 1


            vote_quotients[str(sorted_vote_quotients[0][0])] = vote_quotients[str(sorted_vote_quotients[0][0])] / (current_seats[str(sorted_vote_quotients[0][0])] + 1)
 
    
    # Loops through all parties in the overall seats dictionary, to grab the parties name via id, and insert their total seats.
    for party_id, seats in overall_seats.items():
        # Grabs party name.
        cur.execute("SELECT name FROM parties WHERE id = " + str(party_id))
        party_name = cur.fetchone()

        # Grabs party total votes.
        cur.execute("SELECT SUM(votes) FROM candidates WHERE party_id = " + str(party_id))
        party_votes = cur.fetchone()

        # Inserting the values into the results table.
        cur.execute("INSERT INTO results VALUES ('DHont (by County)', ?, ?, ?, ?, ?)", (party_name[0], seats, round(((seats/650)*100), 2), round((party_votes[0]/votes[0])*100, 2), round(((party_votes[0]/votes[0])*100)-((seats/650)*100), 2)))



    conn.commit()

    # Debugging.

    # Selects all values from results table.
    cur.execute("SELECT * FROM results")
    rows = cur.fetchall()

    # Debugging Print
    for row in rows:
        print(row)

    #closes connection
    conn.close()

if __name__ == '__main__':
    main()
