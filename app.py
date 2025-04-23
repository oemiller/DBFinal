from flask import Flask, render_template, send_file, request
import pg8000
import os
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.colors import CSS4_COLORS
app = Flask(__name__)

def get_column_names(cursor):
    column_names = []
    for column in cursor.description:
        column_names.append(column[0])
    return column_names

def get_data_by_column(all_rows):
    num_rows = len(all_rows)
    num_cols = len(all_rows[0])
    transposed = [[]] * num_cols
    for i in range(len(transposed)):
        transposed[i] = []
    for i in range(num_rows):
        for j in range(num_cols):
            try:
                transposed[j].append(all_rows[i][j])
            except:
                print("ERRORED ON", i, j)
    return transposed

@app.route("/")
def index():
    return render_template("index.html", param="")

@app.route('/plot')
def plot():
    cursor = database_connection.cursor()
    cursor.execute("SELECT * FROM shared_production_and_consumption_by_source") 
    all_rows = cursor.fetchall()
    column_names = get_column_names(cursor)
    cursor.close()
    columns = get_data_by_column(all_rows)
    x = range(len(columns[0])) 
    plt.figure(figsize=(12, 8))
    for i in range(1, len(columns)):
        color = list(CSS4_COLORS.keys())[i]
        plt.plot(x, columns[i], label=column_names[i], color=color, linestyle='--', marker='.')
    plt.title("Production and Consumption by Source")
    plt.xlabel("Months since Jan 1973")
    plt.ylabel("Units of Energy (quadrillion BTUs)")
    plt.legend()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')


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

@app.get("/update_col")
def update_col_get():
    return render_template("update_form_2.html")

@app.post("/update_col")
def update_col_post():

    def check_numeric(x):
        try: 
            a = float(x)
        except:
            return False
        return True
    
    if request.method == 'POST':
        month_yr_in = request.form.get('month_year')
        data=request.form
        print("attempting to update entry where month_year =",month_yr_in)
        for item in data.items():
            colname = item[0]
            colval = item[1]
            if colname != "month_year" and not check_numeric(colval):
                return(render_template("update_form_2.html"))
            print("DATA:", colname, "=", colval)
        return render_template("index.html")
        


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
    cursor.close()
    app.run(debug=False)
