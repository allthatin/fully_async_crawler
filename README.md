
# FULLY ASYNC CRAWLER

This repository contains the code for a web crawler written in Python. It demonstrates asynchronous programming using asyncio to efficiently manage concurrent tasks during the crawling process.

## Requirements
- Python 3.7+
- asyncio
- aiohttp

## Features

- Crawls URLs in an asynchronous manner.
- Groups URLs for efficient processing.
- Handles errors during crawling.
- Stores crawled data in a database (implementation not included).

## Usage:

- Clone the repository:
~~~bash 
git clone https://github.com/allthatin/fully_async_crawler.git
~~~
- Install dependencies:
~~~bash 
pip install -r requirements.txt
~~~
- Configure .env file
- Configure database connection (connection.py)

- Modify the get_async_session function in database/connection.py to connect to your desired database.
- Run the crawler:
~~~bash
python main.py run_worker
~~~

## Code Structure:

- main.py: Entry point for the script.
- database/connection.py: Handles database connection (needs modification).
- management.py: Provides utility functions for command-line execution.
- models.py: Defines data models for storing crawled data (modify for your needs).
- crawlers/base_crawler.py: Abstract base class for defining crawler behavior.
- crawlers/\<specific_crawler>.py: Implementations for specific crawler logic.