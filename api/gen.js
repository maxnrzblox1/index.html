// api/gen.js

const crypto = require('crypto');

// Helper functions
function generateRandomString(length, characters) {
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function generateRandomKey(length = 64) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return generateRandomString(length, characters);
}

function generateRandomNumber(length = 10) {
    const characters = '0123456789';
    return generateRandomString(length, characters);
}

export default function handler(req, res) {
    const service = req.query.service;

    const baseUrls = {
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
    };

    if (baseUrls[service]) {
        let modifiedUrl;
        switch (service) {
            case "fluxus":
            case "delta":
            case "cryptic":
            case "deltaios":
            case "cacti":
                modifiedUrl = baseUrls[service].replace('{}', generateRandomKey());
                break;
            case "arceus":
                modifiedUrl = baseUrls[service].replace('{}', generateRandomKey(16));
                break;
            case "evon":
            case "vegax":
                modifiedUrl = baseUrls[service].replace('{}', generateRandomKey(36));
                break;
            case "trigon":
                const k1 = generateRandomKey(6);
                const k2 = generateRandomKey(4);
                modifiedUrl = baseUrls[service].replace('{}', `${k1}-${k2}-${k2}-${k2}-${k1}`);
                break;
            case "hydrogen":
                modifiedUrl = baseUrls[service].replace('{}', generateRandomNumber());
                break;
            case "relzhub":
                modifiedUrl = baseUrls[service].replace('{}', generateRandomKey(20));
                break;
        }
        return res.status(200).json({ url: modifiedUrl });
    }

    return res.status(400).json({ error: "Failed to generate key, service not found." });
}
