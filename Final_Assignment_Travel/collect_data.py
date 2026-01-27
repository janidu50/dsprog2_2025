import requests
import sqlite3
import time

# Change Line 7 to this:
API_URL = "https://app.rakuten.co.jp/services/api/Travel/KeywordHotelSearch/20170426"
# Your ID goes here (this looks correct based on your screenshot):
APP_ID = "1050736868652427164"
def get_travel_data(keyword="Tokyo"):
    params = {
        "format": "json",
        "keyword": keyword,
        "applicationId": APP_ID,
        "hits": 30 # Get 30 hotels
    }
    
    print(f"Fetching data for {keyword}...")
    response = requests.get(API_URL, params=params)
    
    if response.status_code != 200:
        print(f"Error! Status code: {response.status_code}")
        return None
    
    return response.json()

def save_to_db(data):
    if not data: return

    conn = sqlite3.connect("travel.db")
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            rating REAL
        )
    ''')

    # --- ADJUST THIS PART BASED ON YOUR API ---
    # Rakuten Travel usually has this structure: data['hotels'][i]['hotel'][0]['hotelBasicInfo']
    # If using a different API, print(data) to check the structure.
    
    try:
        hotels_list = data.get('hotels', [])
        for item in hotels_list:
            # Note: Rakuten structure is tricky. It often nests lists inside lists.
            # This logic attempts to find the info.
            info = item['hotel'][0]['hotelBasicInfo']
            
            name = info['hotelName']
            price = info['hotelMinCharge']
            rating = info['reviewAverage']
            
            cursor.execute("INSERT INTO hotels (name, price, rating) VALUES (?, ?, ?)", (name, price, rating))
            
        print(f"Saved {len(hotels_list)} hotels to database.")
        
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        # DEBUG: Uncomment the next line if you get errors, to see what the API gave you
        # print(data)

    conn.commit()
    conn.close()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Get Data
    tokyo_data = get_travel_data("Tokyo")
    save_to_db(tokyo_data)
    
    time.sleep(1) # Be polite to server
    
    osaka_data = get_travel_data("Osaka")
    save_to_db(osaka_data)