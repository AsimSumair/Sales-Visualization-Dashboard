import json
import sqlite3
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import DataPoint  


class Command(BaseCommand):
    help = 'Import data from JSON file into SQLite database'

    def handle(self, *args, **kwargs):
        if DataPoint.objects.exists():
            self.stdout.write(self.style.SUCCESS(""))
            return  

        db_path = settings.DATABASES['default']['NAME']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_datapoint (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            end_year INTEGER,
            intensity INTEGER,
            sector TEXT,
            topic TEXT,
            insight TEXT,
            url TEXT,
            region TEXT,
            start_year TEXT,
            impact TEXT,
            added TEXT,
            published TEXT,
            country TEXT,
            relevance INTEGER,
            pestle TEXT,
            source TEXT,
            title TEXT,
            likelihood INTEGER
        )
        ''')
        
        with open('data/jsondata.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for item in data:
            cursor.execute('''
            INSERT INTO api_datapoint (
                end_year, intensity, sector, topic, insight, url, region, 
                start_year, impact, added, published, country, relevance, 
                pestle, source, title, likelihood
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('end_year'), item.get('intensity'), item.get('sector'), item.get('topic'),
                item.get('insight'), item.get('url'), item.get('region'), item.get('start_year'),
                item.get('impact'), item.get('added'), item.get('published'), item.get('country'),
                item.get('relevance'), item.get('pestle'), item.get('source'), item.get('title'),
                item.get('likelihood')
            ))

        conn.commit()
        conn.close()

        self.stdout.write(self.style.SUCCESS("Data successfully imported into SQLite database!"))
