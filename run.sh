if ping -c 1 https://tranco-list.eu/api/ &> /dev/null
then
    echo "Launching crawler..."
    python3 main.py
else
    echo "Tranco not available"
fi
