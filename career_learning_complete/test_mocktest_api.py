#!/usr/bin/env python3
"""Test the mock test API functionality"""

import requests
import json
import time

# Wait for server to be ready
time.sleep(2)

session = requests.Session()

print("=" * 60)
print("Testing Mock Test API")
print("=" * 60)

# Test without login
print("\n1. Testing GET /api/mocktest/list (without login)")
response = session.get('http://localhost:5000/api/mocktest/list')
print(f"   Status: {response.status_code} (should be 302 for redirect)")

# Login
print("\n2. Testing POST /login with credentials")
login_data = {'username': 'admin', 'password': 'admin123'}
response = session.post('http://localhost:5000/login', data=login_data, allow_redirects=False)
print(f"   Status: {response.status_code} (should be 302)")
print(f"   Cookies: {session.cookies}")

# Get list of tests
print("\n3. Testing GET /api/mocktest/list (after login)")
response = session.get('http://localhost:5000/api/mocktest/list')
print(f"   Status: {response.status_code} (should be 200)")
if response.status_code == 200:
    tests = response.json()
    print(f"   Number of tests: {len(tests)}")
    if tests:
        print(f"   First test: {tests[0]['title']}")
else:
    print(f"   Error: {response.text[:200]}")

# Get specific test
if tests:
    test_id = tests[0]['id']
    print(f"\n4. Testing GET /api/mocktest/{test_id}")
    response = session.get(f'http://localhost:5000/api/mocktest/{test_id}')
    print(f"   Status: {response.status_code} (should be 200)")
    if response.status_code == 200:
        data = response.json()
        print(f"   Test: {data['test']['title']}")
        print(f"   Number of questions: {len(data['questions'])}")
        if data['questions']:
            q = data['questions'][0]
            print(f"   First question: {q['question_text'][:60]}...")
            print(f"   Number of options: {len(q['options'])}")

print("\n" + "=" * 60)
print("✅ Mock Test API tests completed!")
print("=" * 60)
