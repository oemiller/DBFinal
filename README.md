# How to run.

## Install the dependencies manually or use the provided nix shell
* python3 (flask, pg8000, matplotlib)

## Set up your environement file
* copy .env_template to .env
* add your credentials

## Execute the following in your terminal
```
$ source .env && python app.py
*****************************************************************
logged in as oemiller to database csci403 on server ada.mines.edu
*****************************************************************
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

## Visit the site in your browser and enjoy the following endpoints
* /full_table | all data in the table visible from one page
* /year_data | find data from a specific year
* /update_col | update rows in the table
* /plot | displays a graph with energy use by type
