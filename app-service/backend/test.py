import requests

# Make requests
response1 = requests.get("https://xyrm-sqqj-hx6t.n7c.xano.io/api:Dga0jXwg/20207202")
response2 = requests.get("https://xyrm-sqqj-hx6t.n7c.xano.io/api:Dga0jXwg/2021_sch_3")

# Parse JSON responses
data1 = response1.json()
data2 = response2.json()

# Extract email addresses and store in sets to remove duplicates
emails1 = {item.get('Email') for item in data1 if item.get('Email')}
emails2 = {item.get('Email') for item in data2 if item.get('Email')}

# Find the difference in email addresses between the two responses
emails_difference = emails1 - emails2

print("Emails difference (to update Response 1):")
for email in emails_difference:
    print(email)
