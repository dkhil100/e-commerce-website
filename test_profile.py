#!/usr/bin/env python
"""
Test script to verify profile system functionality
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Now import Django models
from django.contrib.auth.models import User
from store.models import UserProfile

def test_profile_system():
    print("Testing Profile System...")
    
    # Test model creation
    try:
        # Check if UserProfile model exists
        print(f"UserProfile model: {UserProfile}")
        print(f"UserProfile fields: {[f.name for f in UserProfile._meta.fields]}")
        
        # Check if we can query (this will fail if migration isn't applied)
        profile_count = UserProfile.objects.count()
        print(f"Current UserProfile count: {profile_count}")
        
        print("✅ Profile system models are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing profile system: {e}")
        return False

if __name__ == '__main__':
    test_profile_system()
