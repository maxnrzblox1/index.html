import fetch from 'node-fetch';
import FingerprintJS from '@fingerprintjs/fingerprintjs';

const DISCORD_BOT_API = 'https://9284a528-8770-4828-9ea1-9e3333a8b142-00-1yp5q41srz8t9.kirk.replit.dev:5000/assign-role';
const API_SECRET = 'maxlol1023';

export default async function handler(req, res) {
  const discord_id = req.query.discord_id;
  if (!discord_id) {
    return res.status(400).send('Missing discord_id');
  }

  // Get IP
  const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;

  // Load fingerprintJS (serverless on Vercel you can init at top-level)
  const fp = await FingerprintJS.load();
  const result = await fp.get();
  const fingerprint = result.visitorId; // unique device id

  try {
    // Send to bot API
    const assignRes = await fetch(DISCORD_BOT_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        secret: API_SECRET,
        discord_id,
        ip,
        fingerprint
      }),
    });

    if (!assignRes.ok) {
      const err = await assignRes.json();
      return res.status(assignRes.status).send(`Verification failed: ${err.error || 'Unknown error'}`);
    }

    return res.status(200).send('✅ Verification successful! You now have access.');
  } catch (error) {
    return res.status(500).send('Server error during verification.');
  }
                         }
