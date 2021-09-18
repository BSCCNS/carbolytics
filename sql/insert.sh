cd ~/data

psql -h localhost -d carbolytics -U data -c "\copy crawl from 'crawl.csv' with csv"
psql -h localhost -d carbolytics -U data -c "\copy dns_responses from 'dns_responses.csv' with csv"