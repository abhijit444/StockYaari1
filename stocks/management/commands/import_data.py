# stocks/management/commands/import_data.py
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from stocks.models import Index, DailyPrice

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to CSV file')
        parser.add_argument('index_name', type=str, help='Name of the index')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        index_name = kwargs['index_name']

        # Create or get the index
        index, created = Index.objects.get_or_create(name=index_name)

        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Trim leading and trailing spaces from column names
                row = {key.strip(): value for key, value in row.items()}

                # Assuming the date format is 'DD-MMM-YYYY'
                date_str = row['Date']
                date_obj = datetime.strptime(date_str, '%d-%b-%Y').date()

                DailyPrice.objects.create(
                    index=index,
                    date=date_obj,
                    open_price=row['Open'],
                    high_price=row['High'],
                    low_price=row['Low'],
                    close_price=row['Close'],
                    shares_traded=row['Shares Traded'],
                    turnover=row['Turnover (₹ Cr)']
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
