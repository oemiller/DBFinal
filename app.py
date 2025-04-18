from flask import Flask, render_template
import pg8000
import os

app = Flask(__name__)
database_connection = None

@app.route("/")
def index():
    return render_template("index.html", param="")

@app.route("/test")
def test():
    return render_template("index.html", param="")

if __name__ == "__main__":
    try:
        user     = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        host     = os.environ["POSTGRES_HOST"]
        database = os.environ["POSTGRES_DB"]
    except:
        print("did you forget to load your environment file?")
        print("$ source .env && python app.py")
        exit()
    welcome_string = "logged in as " + user + " to database " + database + " on server " + host
    banner = "*" * len(welcome_string)
    print(banner)
    print(welcome_string)
    print(banner)
    database_connection = pg8000.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )
    cursor = database_connection.cursor()
    cursor.execute("SET search_path TO group39") 
    cursor.execute("SELECT * FROM test_table") 
    result = cursor.fetchall() 
    print("query result", result)
    app.run(debug=False)
