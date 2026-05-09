import requests

FAST2SMS_KEY = "wlh0bTX7H9xtBIWK2JOpUCjPNc6RLraVMSYGfmQDi5knevz3E80jd7McFmQ8XlkUNe3DwvfpGyz9rxCZ"

def test_sms():
    url = "https://www.fast2sms.com/dev/bulkV2"
    otp = "123456"
    phone = "7200575426" 
    
    # Using 'q' route for Quick SMS
    payload = {
        "route": "q",
        "message": f"Your Smart AI Farm OTP is: {otp}",
        "language": "english",
        "numbers": phone,
    }
    headers = {
        "authorization": FAST2SMS_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    print(f"Sending OTP {otp} to {phone} using Quick SMS route...")
    response = requests.post(url, data=payload, headers=headers)
    print("Response Status:", response.status_code)
    try:
        print("Response Body:", response.json())
    except:
        print("Response Text:", response.text)

if __name__ == "__main__":
    test_sms()
