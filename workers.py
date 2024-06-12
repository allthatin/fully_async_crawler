import asyncio, random
from sqlalchemy import select
from database.models import CrawlingUrl
from sites.base import BaseCrawler
from typing import Optional, Callable


async def initialize(session):
    stmt = select(CrawlingUrl).where(CrawlingUrl.instock == False)
    result = await session.execute(stmt)
    urls = result.scalars().all()
    return urls

async def crawl_website(url: str, crawler: BaseCrawler):
    """
    Crawls the specified URLs using the provided crawler class.

    Args:
        urls: The URLs to be crawled.
        session: The database session object.
        crawler: The crawler class to be used.
    """
    
    try:
        data = await crawler().crawl(url)
        return data
    except Exception as e:
        print(f"Error: {url} - {e}")
        return []

def get_crawler(url: str) -> Optional[Callable]:
    """
    Determines the appropriate crawler class based on the URL.

    Args:
        url: The URL to be crawled.

    Returns:
        The crawler class to be used, or None if no matching crawler is found.
    """
    # Implement your logic to map URLs to specific crawler classes (e.g., dictionary lookup)
    if "api.ingka.ikea.com" in url:
        from sites.ikea import IkeaCrawler  # Assuming IkeaCrawler is defined in ikea.py
        return IkeaCrawler
    return None

async def worker(session):
    """
    Manages the crawling process, including URL retrieval, grouping, and crawling logic.

    Args:
        session: The database session object.
    """
    while True:
        print("\n\n\n\n\n\n")
        print("Starting CRAWLER ENGINE...")
        urls = await initialize(session)
        print(f"Found {len(urls)} URLs to crawl.")
        if not urls:
            print("No URLs to crawl. Sleeping for 5 minutes...")
            await asyncio.sleep(300)
            continue

        chunk_size = 10  # Number of URLs to process concurrently
        grouped_urls = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
        print(f"Number of Group : {len(grouped_urls)} Total URL : {len(urls)}")

        for url_group in grouped_urls:
            tasks = []
            for url in url_group:
                crawler = get_crawler(url.url)
                if crawler:
                    tasks.append(crawl_website(url.url, crawler))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result, url in zip(results, url_group):
                if isinstance(result, Exception):  # If the task raised an exception
                    print(f"Error crawling URL: {url.url} - Error: {result}")
                else:
                    print(f"URL: {url.url} - Result: {result}")
                    url.stockdata = str(result)  # Convert the list of dictionaries to a string
                    url.instock = bool(result)
                    session.add(url)
        await session.commit()
        await asyncio.sleep(random.randint(60, 120))