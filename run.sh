echo "Fetching data from tranco-list.eu ..."
wget https://tranco-list.eu/download/VJ6N/1000000 -O top1M.csv -q

echo "Launching crawler..."
python3 setup.py

echo "DONE..."
