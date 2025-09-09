#!/bin/bash

# Script to fix Neon PostgreSQL connection issues on PythonAnywhere

echo "🔍 Checking Neon PostgreSQL connection..."

# Test connection to Neon database
echo "📡 Testing database connection..."

python3 << 'EOF'
import psycopg2
import os

# Database connection parameters
conn_params = {
    'host': 'ep-shy-hat-a9wddu9f-pooler.gwc.azure.neon.tech',
    'port': '5432',
    'dbname': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_gDbsPZxln7I5',
    'sslmode': 'require'
}

try:
    print("Attempting to connect to Neon PostgreSQL...")
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f"✅ Database connection successful!")
    print(f"PostgreSQL version: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("🔧 Possible solutions:")
    print("1. Check if Neon database is in sleep mode")
    print("2. Verify connection credentials")
    print("3. Check firewall settings")
    print("4. Try using different host endpoint")
EOF

echo "🔄 If connection failed, the database might be sleeping..."
echo "💡 Log into your Neon console to wake it up or check the connection string"
