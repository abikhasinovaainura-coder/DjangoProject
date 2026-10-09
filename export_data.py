import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')
django.setup()

with open('data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'core', indent=2, stdout=f)

print("Деректер data.json файлына UTF-8 форматында сәтті сақталды!")