import fetch from 'node-fetch';

const DISCORD_BOT_API = 'http://YOUR_BOT_SERVER_IP:5000/assign-role';
const API_SECRET = 'YOUR_SECRET_KEY';

export default async function handler(req, res) {
  const discord_id = req.query.discord_id;
  if (!discord_id) {
    return res.status(400).send('Missing discord_id');
  }

  const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;

  try {
    const assignRes = await fetch(DISCORD_BOT_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        secret: API_SECRET,
        discord_id,
        ip
      }),
    });

    if (!assignRes.ok) {
      const err = await assignRes.json();
      return res.status(assignRes.status).send(`
        <html>
          <body style="font-family:sans-serif;text-align:center;">
            <h1>❌ Verification failed</h1>
            <p>${err.error || 'Unknown error'}</p>
          </body>
        </html>
      `);
    }

    return res.status(200).send(`
      <html>
        <body style="font-family:sans-serif;text-align:center;">
          <h1>✅ Verification successful!</h1>
          <p>You now have access to the server.</p>
        </body>
      </html>
    `);
  } catch (error) {
    return res.status(500).send(`
      <html>
        <body style="font-family:sans-serif;text-align:center;">
          <h1>⚠️ Server error during verification</h1>
          <p>${error.message}</p>
        </body>
      </html>
    `);
  }
}
