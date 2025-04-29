1. Install Logstash, ElasticSearch, Kibana
    Create index in ElasticSearch
2. The Logstash RSS input plugin needs to be installed. 
3. Use rss-feed.conf to run Logstash, for news API data, use newsapi.conf
4. View data in Kibana to see if all the data are coming in normally and check
    if the mapping matches the two mappings we provide
5. Run the python program for AI summarization
6. Import Saved Objects (dashboard.ndjson) and the UI will show up in Kibana dashboard 
