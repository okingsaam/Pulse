#!/usr/bin/env python
"""
Script para testar views do Django
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulse_project.settings')
django.setup()

from core.views import dashboard
from django.test import RequestFactory

def test_dashboard():
    """Testar view dashboard"""
    try:
        factory = RequestFactory()
        request = factory.get('/')
        
        response = dashboard(request)
        print(f"✅ Dashboard OK - Status: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no dashboard: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_dashboard()