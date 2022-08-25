# fampay-video-fetcher

A youtube videos fetcher written in Python's Django Restframework. The following lines describe the structure of the application:
- Contains an asynchronous celery beat scheduled task that runs every 10 seconds. This fetches the youtube data v3 api for the videos based on the query provides in the .env file. The results are saved to the database.
- We can get the fetched results through `/api/fetch/?page=<PAGE NUMBER>`.
- We can search for a different query in the fetched results through `/api/search/?page=<PAGE NUMBER>&query=<SEARCH QUERY>`.
