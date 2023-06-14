import platform
from datetime import datetime, timedelta
from time import time
import json
import aiohttp
import asyncio
import sys


async def main(days):

    async with aiohttp.ClientSession() as session:
        api = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
        now = datetime.now()
        result = []
        for day in range(days):
            days_delta = timedelta(days=day)
            date = str((now - days_delta).strftime('%d.%m.%Y'))

            async with session.get(api + date) as response:
                response_data = await response.json()

                exchange_rates = response_data['exchangeRate']

                daily_rates = {}
                for rate in exchange_rates:
                    if rate['currency'] in ['EUR', 'USD']:
                        currency = rate['currency']
                        sale_rate = rate['saleRate']
                        purchase_rate = rate['purchaseRate']
                        daily_rates[currency] = {
                            'sale': sale_rate, 'purchase': purchase_rate}

                item = {date: daily_rates}
                result.append(item)

        output = json.dumps(result, indent=2)
        print(output)

if __name__ == "__main__":
    days = int(sys.argv[1])
    if days <= 10:
        timer = time()
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main(days))
        print(f'Done by time: {round(time() - timer, 4)}')
    else:
        print('Try 10 days or less next time')
