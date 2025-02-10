require('dotenv').config();
const fetch = require('node-fetch');

exports.handler = async function () {
    try {
        const response = await fetch('https://api.petfinder.com/v2/oauth2/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                grant_type: 'client_credentials',
                client_id: process.env.PETFINDER_API_KEY,
                client_secret: process.env.PETFINDER_API_SECRET
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Adding CORS headers to the response
        return {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin": "*",  // You can replace '*' with your GitHub Pages URL if needed
                "Access-Control-Allow-Methods": "GET, POST",  // Allowing the GET and POST methods
                "Access-Control-Allow-Headers": "Content-Type",  // Allowing Content-Type header
            },
            body: JSON.stringify({ accessToken: data.access_token }),
        };
        
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
