import csv
from django.core.management.base import BaseCommand
from dashboard.models import MarketTrend

class Command(BaseCommand):
    help = 'Import market trend data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('ai_market_trends.csv', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['ai_market_trends.csv']
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Extract data
                year = int(row['Year'])
                category = row['Category']
                market_share = float(row['Market Share'])
                
                # Create or update the model instance
                MarketTrend.objects.update_or_create(
                    year=year,
                    category=category,
                    defaults={'market_share': market_share}
                )
                
        self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))
