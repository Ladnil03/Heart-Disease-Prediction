/**
 * config.js — API configuration
 *
 * Centralises the API base URL. The API key is no longer hardcoded;
 * instead, initAPIKey() fetches a short-lived signed token from the
 * backend's GET /api/token endpoint on page load.
 */
// Fixes: FIX-1 (remove hardcoded key, fetch token instead), FIX-2 (no script.js reference)

const API_CONFIG = {
    baseURL: getAPIBaseURL(),
    apiKey: null,          // populated by initAPIKey()
};

/**
 * Fetch a short-lived signed token from the backend and store it in
 * API_CONFIG.apiKey. Must be awaited before the first API call.
 */
async function initAPIKey() {
    try {
        const res = await fetch(`${API_CONFIG.baseURL}/api/token`);
        if (!res.ok) throw new Error(`token fetch failed: ${res.status}`);
        const { token } = await res.json();
        API_CONFIG.apiKey = token;
    } catch (e) {
        console.error('Could not retrieve API token:', e);
    }
}

/**
 * Determine the correct API base URL based on the current hostname.
 */
function getAPIBaseURL() {
    // Allow override from index.html <script> block
    if (window.__ENV__ && window.__ENV__.API_URL && window.__ENV__.API_URL !== 'https://your-api-domain.vercel.app') {
        return window.__ENV__.API_URL;
    }

    // Local development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:8000';
    }

    // Production: Render backend URL
    return 'https://heart-disease-prediction-h2kn.onrender.com';
}
