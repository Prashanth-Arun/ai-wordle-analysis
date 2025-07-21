import requests
import sys

# Placeholding value
date = "11"
month = "07"
wordle_number = "1484"

n = len(sys.argv)
if n != 4:
    print("Usage: wordle_stat.py MM DD WNUM")
    exit()

month = sys.argv[1]
date = sys.argv[2]
wordle_number = sys.argv[3]

url = "https://www.nytimes.com/2025/{0}/{1}/crosswords/wordle-review-{2}.html?partnership=discord".format(month, date, wordle_number)

print(url)
# Try with mobile user-agent
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    
    if "Please verify you're human" in response.text:
        print("Blocked by CAPTCHA")
    elif response.status_code == 200:
        # Try to find the text
        if "Today’s average difficulty" in response.text:
            start = response.text.find("Today’s average difficulty")
            end = response.text.find("</strong>", start)
            print(response.text[start:end])
        else:
            print("Text not found in response")
    else:
        print(f"Failed with status: {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
