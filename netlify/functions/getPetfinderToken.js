const fetch = require("node-fetch");

exports.handler = async function () {
  const apiKey = process.env.PETFINDER_API_KEY;
  const apiSecret = process.env.PETFINDER_API_SECRET;

  const response = await fetch("https://api.petfinder.com/v2/oauth2/token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      grant_type: "client_credentials",
      client_id: apiKey,
      client_secret: apiSecret,
    }),
  });

  const data = await response.json();
  
  return {
    statusCode: 200,
    body: JSON.stringify({ accessToken: data.access_token }),
  };
};
