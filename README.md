Trafi Open Data about Finnish vehicles into PostgreSQL



## Usage

Download CSV of Open Data from here:
https://www.trafi.fi/tietopalvelut/avoin_data


Check vehicle counts and filter some years
           python3 filter_data.py --laske 2000 open_data_file.csv

           python3 filter_data.py --suodata 2000 open_data_file.csv


Generate file for SQL import
           python3 sql_import.py open_data_file.csv_filtered > 002_insert_data.sql



Insert data into PostgreSQL

For example with username user and host localhost and databasename opendata use commands like this

           psql user -h localhost -d opendata -f 001_create_table.sql

           psql user -h localhost -d opendata -f 002_insert_data.sql
