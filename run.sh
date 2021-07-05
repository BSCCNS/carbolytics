# echo "Fetching data from tranco-list.eu ..."
# wget https://tranco-list.eu/top-1m.csv.zip -O top1M.zip
# unizp top1M.zip
# rm top1M.zip

echo "Launching crawler..."
cp setup.py -r OpenWPM/
cd OpenWPM
python setup.py

echo "Cleaning OpenWPM folder ..."
rm setup.py

echo "Compressing data ..."
cd ../
tar -czf data.tar.gz data
# rm data
