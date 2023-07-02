import requests

url = 'http://192.168.1.166:5000/control_gpio'  # Replace <API_HOST> with the actual host or IP address

switch = '1'
func = '0'

payload = {
    'switch': switch,
    'func': func
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print('GPIO control executed')
else:
    print('Error executing GPIO control:', response.text)
