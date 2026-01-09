import requests
import sqlite3
import time
from datetime import datetime
import json

BASE_URL = "http://localhost:5000"
DB_PATH = "users.db"

def check_db_word_of_day():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM word_of_day_history WHERE date = date('now')")
    row = cursor.fetchone()
    conn.close()
    return row

def check_db_related_words(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM related_words_cache WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def verify_word_of_day():
    print("\n--- Verifying Word of the Day ---")
    
    # 1. Initial Call (should trigger API and DB insert)
    print("1. Calling /word_of_day (First time)...")
    start = time.time()
    resp = requests.get(f"{BASE_URL}/word_of_day")
    elapsed1 = time.time() - start
    print(f"   Status: {resp.status_code}, Time: {elapsed1:.2f}s")
    if resp.status_code != 200:
        print("   FAILED: API error")
        return
    word1 = resp.json().get('word')
    print(f"   Word: {word1}")

    # 2. Verify DB persistence
    row = check_db_word_of_day()
    if row and row['word'] == word1:
        print("   SUCCESS: Word persisted to DB.")
    else:
        print(f"   FAILED: Word not found in DB. Found: {row['word'] if row else 'None'}")

    # 3. Second Call (should be fast and same word)
    print("2. Calling /word_of_day (Second time)...")
    start = time.time()
    resp = requests.get(f"{BASE_URL}/word_of_day")
    elapsed2 = time.time() - start
    print(f"   Status: {resp.status_code}, Time: {elapsed2:.2f}s")
    word2 = resp.json().get('word')
    
    if word1 == word2:
        print("   SUCCESS: Word matches cached value.")
    else:
        print("   FAILED: Word changed (Cache miss?)")

    if elapsed2 < elapsed1: # Not a perfect check but usually cache is faster
        print("   Performance: Second call was faster.")

def verify_related_words():
    print("\n--- Verifying Related Words ---")
    user_id = 1
    
    # Ensure user exists or just rely on fake user_id if DB constraint allows? 
    # The schema has FOREIGN KEY so we need a valid user.
    # Assuming user 1 exists from previous runs, traversing auth flow might be needed if not.
    # Let's try to query /stats first to see if user 1 works.
    resp = requests.get(f"{BASE_URL}/stats?user_id={user_id}")
    if resp.status_code != 200:
        print("   User 1 might not exist. Creating temporary user...")
        # Create user code here if needed, but for now assuming user 1 exists.
    
    # 1. First Call
    print("1. Calling /related_words (First time - might be slow)...")
    start = time.time()
    resp = requests.get(f"{BASE_URL}/related_words?user_id={user_id}")
    elapsed1 = time.time() - start
    print(f"   Status: {resp.status_code}, Time: {elapsed1:.2f}s")
    data1 = resp.json()
    
    # 2. Verify DB persistence
    row = check_db_related_words(user_id)
    if row:
        print("   SUCCESS: Related words persisted to DB.")
    else:
        print("   FAILED: No cache entry found.")

    # 3. Second Call (Cached)
    print("2. Calling /related_words (Second time)...")
    start = time.time()
    resp = requests.get(f"{BASE_URL}/related_words?user_id={user_id}")
    elapsed2 = time.time() - start
    print(f"   Status: {resp.status_code}, Time: {elapsed2:.2f}s")
    
    if elapsed2 < 2.0: # Arbitrary threshold, API usually takes > 2s
        print("   SUCCESS: Fast response indicates cache hit.")
    else:
        print("   WARNING: Response took long, might have hit API.")

if __name__ == "__main__":
    try:
        verify_word_of_day()
        verify_related_words()
    except Exception as e:
        print(f"Verification script failed: {e}")
