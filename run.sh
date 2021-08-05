brows=N_BROWSERS

echo "Fetching data from tranco-list.eu ..."
wget https://tranco-list.eu/top-1m.csv.zip -O top1M.zip -q
echo "Unzip file ..."
unzip top1M.zip

head -n $N_WEBS top-1m.csv >top1M.csv

echo "Launching crawler..."
python3 main.py

echo "DONE..."
