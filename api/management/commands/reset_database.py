from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Resets the database completely by dropping all tables, doing the migrations, and loading back the data'

    def handle(self, *args, **options):
        self.stdout.write('Resetting database...')
        try:
            with connection.cursor() as cursor:
                cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'error:{e}'))
            return
        
        self.stdout.write(self.style.SUCCESS('Successfully reset the database.'))
        self.stdout.write('Migrating tables...')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrations complete'))
        try:
            call_command('load_data')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'error:{e}'))
            return
        self.stdout.write(self.style.SUCCESS('Loding data complete'))