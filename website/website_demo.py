from flask import Flask, render_template
import sqlite3 

app = Flask(__name__, template_folder='templates', static_folder='static') 

with app.app_context():
    @app.route('/')
    def index():
        website_text = '<h1>Results</h1>'
    
    
    
        conn = sqlite3.connect(r"C:\Users\charl\Documents\GitHub\S2Database2ndYear\data\pythonsqlite.db")
        cur = conn.cursor()
        
        website_text += '<table>'
        website_text += '<thead>'
        website_text += '<th>Party</th>'
        website_text += '<th>Seats</th>'
        website_text += '<th>Seats Percent(%)</th>'
        website_text += '<th>Vote Percent(%)</th>'
        website_text += '<th>Difference(%)</th>'
        website_text += '</thead>'
        website_text += '<tbody>'
        
        previoussystem = 'None'
        systemindex = 0
        for row in cur.execute("SELECT * FROM results"):
            if str(row[0]) != previoussystem:                 
                 systemindex += 1
            website_text += '<tr class="system' + str(systemindex) + '">'
            for item in row:
                if item == row[0]:
                     continue
                website_text += '<td>' + str(item) + '</td>'
            website_text += '</tr>'
            previoussystem = str(row[0])
        website_text += '</tbody>'
        cur.close()

        
        return render_template('index.html', table=website_text)

    
    
    


if __name__ == '__main__': 
	app.run(debug=False) 
