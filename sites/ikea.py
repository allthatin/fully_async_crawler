from sites.base import BaseCrawler
from typing import Dict, List

class IkeaCrawler(BaseCrawler):
    """
    Concrete crawler class for handling IKEA API interactions.
    """

    CONFIG = {
        'base_url': "https://api.ingka.ikea.com/cia/availabilities/",
        'headers': {
        "accept": "application/json;version=2",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        
        }
    }

    def parse_stock(self, data: Dict) -> List[Dict]:
        """
        Parses IKEA API response data to extract stock information.

        Args:
            data: The JSON data received from the IKEA API.

        Returns:
            A list of dictionaries containing stock information for individual items.
        """
        # Implement your specific parsing logic here (same as before)
        availabilities = data.get('availabilities', [])
        stock_info = []
        for availability in availabilities:
            item_info = {}
            item_info['itemNo'] = availability.get('itemKey', {}).get('itemNo')
            item_info['itemType'] = availability.get('itemKey', {}).get('itemType')
            item_info['availableForCashCarry'] = availability.get('availableForCashCarry', False)
            cash_carry_info = availability.get('buyingOption', {}).get('cashCarry', {})
            item_info['quantity'] = cash_carry_info.get('availability', {}).get('quantity', 0)
            restocks = cash_carry_info.get('restocks', [])
            if restocks:
                item_info['restockDate'] = restocks[0].get('earliestDate')
                item_info['restockQuantity'] = restocks[0].get('quantity')
            
            if item_info['quantity'] > 0:
                item_info['storeInfo'] = self.parse_store_info(data, availability.get('classUnitKey', {}).get('classUnitCode'))
                stock_info.append(item_info)
            
        return stock_info
    
    def parse_store_info(self, data, class_unit_code):
        sales_locations = data.get('salesLocations', [])
        for location in sales_locations:
            if location.get('classUnitKey', {}).get('classUnitCode') == class_unit_code:
                return location.get('salesLocations', [])
        return []

    async def crawl(self, url: str) -> List[Dict]:
        """
        Crawls the IKEA API endpoint and returns extracted stock information.

        Args:
            url: The IKEA API URL to crawl.

        Returns:
            A list of dictionaries containing stock information for individual items.
        """
        data = await self.fetch_data(url)
        if data:
            return self.parse_stock(data)
        else:
            return []