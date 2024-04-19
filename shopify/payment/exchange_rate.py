import aiohttp


from bs4 import BeautifulSoup





HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}


async def get_exchange_rate(base: str = 'USD', target: str = 'RUB') -> float:
    """Get exchange rate from myfin.by."""
    url = f'https://myfin.by/converter/{base.lower()}-{target.lower()}'
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), 'html.parser')
            element = soup.find('input', {'id': 'to_input_curr'})
            if element is None:
                raise RuntimeError('Element not found in HTML')
            return float(element['value'])
    except aiohttp.ClientResponseError as e:
        raise RuntimeError(
            f'Failed to get exchange rate from {url}: {e.status}') from e
    except aiohttp.ClientError as e:
        raise RuntimeError(
            f'Failed to get exchange rate from {url}: {e}') from e
    except (TypeError, ValueError) as e:
        raise RuntimeError(
            f'Failed to parse exchange rate from {url}: {e}') from e
