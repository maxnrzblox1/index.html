from urllib.parse import parse_qs

def generate_random_string(length, characters):
    import random
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_key(length=64):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return generate_random_string(length, characters)

def generate_random_number(length=10):
    characters = '0123456789'
    return generate_random_string(length, characters)

def handler(request):
    query = parse_qs(request['queryStringParameters'] or {})
    service = query.get('service', [None])[0]

    base_urls = {
        "fluxus": "https://flux.li/android/external/start.php?HWID={}",
        "delta": "https://gateway.platoboost.com/a/8?id={}",
        "cryptic": "https://gateway.platoboost.com/a/39097?id={}",
        "evon": "https://pandadevelopment.net/getkey?service=evon&hwid={}",
        "cacti": "https://gateway.platoboost.com/a/23344?id={}",
        "hydrogen": "https://gateway.platoboost.com/a/2569?id={}",
        "relzhub": "https://getkey.relzscript.xyz/redirect.php?hwid={}",
        "vegax": "https://pandadevelopment.net/getkey?service=vegax&hwid={}&provider=linkvertise",
        "deltaios": "https://gateway.platoboost.com/a/2?id={}",
        "arceus": "https://spdmteam.com/key-system-1?hwid={}&zone=Europe/Rome&os=android",
        "trigon": "https://trigonevo.fun/whitelist/?HWID={}-{}-{}-{}-{}"
    }

    if service in base_urls:
        if service in ["fluxus", "delta", "cryptic", "deltaios", "cacti"]:
            hwid = generate_random_key()
            url = base_urls[service].format(hwid)
        elif service == "arceus":
            url = base_urls[service].format(generate_random_key(16))
        elif service in ["evon", "vegax"]:
            url = base_urls[service].format(generate_random_key(36))
        elif service == "trigon":
            k1 = generate_random_key(6)
            k2 = generate_random_key(4)
            url = base_urls[service].format(k1, k2, k2, k2, k1)
        elif service == "hydrogen":
            url = base_urls[service].format(generate_random_number())
        elif service == "relzhub":
            url = base_urls[service].format(generate_random_key(20))
        return {
            "statusCode": 200,
            "body": f'{{"url": "{url}"}}',
            "headers": { "Content-Type": "application/json" }
        }

    return {
        "statusCode": 400,
        "body": '{"error": "Invalid service"}',
        "headers": { "Content-Type": "application/json" }
    }
