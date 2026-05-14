import os
import sys
# Ensure project root is on path so Django can import myproject
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')
import django
django.setup()
from django.urls import get_resolver
resolver = get_resolver()
for key in sorted(resolver.reverse_dict.keys(), key=lambda x: str(x)):
    print(repr(key))
