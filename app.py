from flask import Flask, render_template
from flask import request
import pg8000
import os

app = Flask(__name__)

def get_column_names(cursor):
    column_names = []
    for column in cursor.description:
        column_names.append(column[0])
    return column_names


@app.route("/")
def index():
    return render_template("index.html", param="")

@app.route("/full_table")
def full_table():
    cursor = database_connection.cursor()
    cursor.execute("SELECT * FROM shared_production_and_consumption_by_source") 
    all = cursor.fetchall()
    column_names = get_column_names(cursor)
    cursor.close()
    return render_template("full_table.html", column_names=column_names, items=all)

@app.route("/test")
def test_page():
    return render_template("index.html", param="")

@app.get("/year_data")
def year_get():
    return render_template("year_form.html")

@app.post("/year_data")
def year_post():
    if request.method == 'POST':
        year_in = request.form.get('year')
        query = """
            SELECT * FROM shared_production_and_consumption_by_source
            WHERE month_year LIKE %s
        """
        cursor = database_connection.cursor()
        cursor.execute(query, (str(year_in)[:4] + '%',))
        all = cursor.fetchall()
        column_names = get_column_names(cursor)
        cursor.close()
        return render_template("full_table.html", column_names=column_names, items=all)



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
    print(type(database_connection))
    cursor = database_connection.cursor()
    cursor.execute("SET search_path TO group39") 
    cursor.close()
    app.run(debug=False)
