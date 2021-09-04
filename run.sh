sleep 1m
echo "Launching crawler..."
python3 main.py

cd ~/data

bash ~/OpenWPM/exportSQLite.sh crawl-data.sqlite
rm crawl-data.sqlite

echo "DONE..."
