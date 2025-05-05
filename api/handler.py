import random
import string
from typing import Dict, Any

# Function to generate a random string of a given length and characters
def generate_random_string(length: int, characters: str) -> str:
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate a random key (default length 64, characters A-Z, a-z, 0-9)
def generate_random_key(length: int = 64, characters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') -> str:
    return generate_random_string(length, characters)

# Function to generate a random number string (default length 10)
def generate_random_number(length: int = 10) -> str:
    return generate_random_string(length, '0123456789')

# Function to handle the request and generate a modified URL
def handler(request: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
    # Check if the method is GET
    if request['method'] != 'GET':
        response['statusCode'] = 405
        response['body'] = {"error": "Method not allowed"}
        return response

    # Extract the 'service' query parameter
    service = request.get('query', {}).get('service')

    base_urls: Dict[str, str] = {
        'fluxus': 'https://flux.li/android/external/start.php?HWID={}',
        'delta': 'https://gateway.platoboost.com/a/8?id={}',
        'cryptic': 'https://gateway.platoboost.com/a/39097?id={}',
        'evon': 'https://pandadevelopment.net/getkey?service=evon&hwid={}',
        'cacti': 'https://gateway.platoboost.com/a/23344?id={}',
        'hydrogen': 'https://gateway.platoboost.com/a/2569?id={}',
        'relzhub': 'https://getkey.farrghii.com/redirect.php?hwid={}',
        'vegax': 'https://pandadevelopment.net/getkey?service=vegax&hwid={}&provider=linkvertise',
        'deltaios': 'https://gateway.platoboost.com/a/2?id={}',
        'arceus': 'https://spdmteam.com/key-system-1?hwid={}&zone=Europe/Rome&os=android',
        'trigon': 'https://trigonevo.fun/whitelist/?HWID={}-{}-{}-{}-{}',
    }

    if not service or service not in base_urls:
        response['statusCode'] = 400
        response['body'] = {"error": "Failed to generate key, service not found."}
        return response

    # Start generating the modified URL based on the service
    modified_url = ''
    
    if service in ['fluxus', 'delta', 'cryptic', 'deltaios', 'cacti']:
        modified_url = base_urls[service].replace('{}', generate_random_key())
    elif service == 'arceus':
        modified_url = base_urls[service].replace('{}', generate_random_key(16))
    elif service in ['evon', 'vegax']:
        modified_url = base_urls[service].replace('{}', generate_random_key(36))
    elif service == 'trigon':
        r1 = generate_random_key(6)
        r2 = generate_random_key(4)
        modified_url = base_urls[service].replace('{}', r1).replace('{}', r2).replace('{}', r2).replace('{}', r2).replace('{}', r1)
    elif service == 'hydrogen':
        modified_url = base_urls[service].replace('{}', generate_random_number())
    elif service == 'relzhub':
        modified_url = base_urls[service].replace('{}', generate_random_key(20))

    response['statusCode'] = 200
    response['body'] = {"url": modified_url}
    return response
  
