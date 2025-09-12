#!/usr/bin/env python3
import requests

def test_server():
    try:
        response = requests.get('https://sinanej2.pythonanywhere.com/api/health/', timeout=10)
        print(f'Status Code: {response.status_code}')
        print(f'Headers: {dict(response.headers)}')
        print(f'Content: {response.text[:1000]}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    test_server()
