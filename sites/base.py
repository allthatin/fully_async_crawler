from abc import ABC, abstractmethod
from typing import Dict, List, Union
from aiohttp import ClientSession, ClientTimeout

class BaseCrawler(ABC):
    """
    Abstract base class for defining crawler behavior with pluggable options.
    """
    CONFIG = {} 
    def __init__(self, config: Dict = None):
        """
        Initializes the crawler with optional configuration.

        Args:
            config (Dict, optional): A dictionary containing configuration options.
                                    Defaults to None, which uses the class-level CONFIG.
        """
        self.config = config or self.CONFIG

    @abstractmethod
    async def crawl(self, url: str) -> List[Dict]:
        """
        Crawls the given URL and returns extracted data.

        Args:
            url: The URL to be crawled.

        Returns:
            A list of dictionaries containing extracted data.
        """
        raise NotImplementedError

    async def fetch_data(self, url: str) -> Union[Dict, None]:
        """
        Fetches data from the given URL using configured headers.

        Args:
            url: The URL to fetch data from.

        Returns:
            A dictionary containing the fetched data (if successful), 
            or None otherwise.
        """
        async with ClientSession(timeout=ClientTimeout(total=2)) as session:
            async with session.get(url, headers=self.config.get('headers', {})) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    print(f"Error: {self.__class__.__name__} - {url} - Status code {resp.status}")
                    return None