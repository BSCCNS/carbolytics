cd ../data

# Remove previous CSV
rm -rf *.csv -f

# obtains all data tables from database
TS=$(sqlite3 $1 "SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name not like 'sqlite_%';")

# exports each table to csv
for T in $TS; do

    sqlite3 $1 <<!
.headers on
.mode csv
.output $T.csv
select * from $T;
!

# Remove SQLite3
rm -rf *.sqlite

done
