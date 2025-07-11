import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from dashboard.models import MarketTrend
class Command(BaseCommand):
    help = 'Scrape AI market trends and save to database'

    def handle(self, *args, **options):
        #url = 'https://www.gartner.com/en/insights/artificial-intelligence'
        url = 'https://www.gartner.com/en/information-technology/insights/artificial-intelligence'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extract data (update selectors as needed)
        data = []
        for trend in soup.find_all('div', class_='trend-item'):  # Adjust class as necessary
            year = trend.find('span', class_='year').get_text(strip=True)
            category = trend.find('span', class_='category').get_text(strip=True)
            market_share = trend.find('span', class_='market-share').get_text(strip=True).strip('%')
            data.append({
                'year': int(year),
                'category': category,
                'market_share': float(market_share)
            })

        # Save to database
        for entry in data:
            MarketTrend.objects.update_or_create(
                year=entry['year'],
                category=entry['category'],
                defaults={'market_share': entry['market_share']}
            )
        self.stdout.write(self.style.SUCCESS('Data scraped and saved successfully'))
