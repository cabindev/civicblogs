#!/usr/bin/env python3
"""
Test script to check Supabase connectivity
"""
import os
import sys
import django
from decouple import config

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicblogs.settings')
sys.path.append('/Applications/MAMP/htdocs/civicblogs')
django.setup()

def test_supabase_connection():
    """Test different ways to connect to Supabase"""
    
    # Connection strings to try
    connection_strings = [
        # Correct Supabase pooler (from user)
        'postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true',
        
        # Direct connection (from user)
        'postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres',
        
        # Alternative without pgbouncer
        'postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres',
        
        # With SSL
        'postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require',
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"\n🔍 Testing connection {i}: {conn_str.split('@')[1].split('/')[0]}...")
        
        try:
            import psycopg2
            conn = psycopg2.connect(conn_str, connect_timeout=10)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            print(f"✅ SUCCESS! Connected to PostgreSQL")
            print(f"   Version: {result[0]}")
            print(f"   Connection string: {conn_str}")
            return conn_str
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            continue
    
    print("\n🚫 All connection attempts failed!")
    return None

def test_django_connection():
    """Test Django database connection"""
    from django.db import connection
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Django database connection successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Django database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔗 Testing Supabase Database Connectivity")
    print("=" * 50)
    
    # Test direct PostgreSQL connection
    working_conn_str = test_supabase_connection()
    
    if working_conn_str:
        print(f"\n📝 Update your .env file with:")
        print(f"DATABASE_URL={working_conn_str}")
        
        print(f"\n🧪 Testing Django connection...")
        test_django_connection()
    else:
        print("\n💡 Suggestions:")
        print("1. Check if your network allows connections to Supabase")
        print("2. Verify your Supabase credentials")
        print("3. Try using a VPN if behind corporate firewall")
        print("4. Use SQLite for local development (set USE_POSTGRES=False)")