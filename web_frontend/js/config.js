/**
 * config.js — API configuration
 *
 * Centralises the API base URL and API key so they are defined in
 * one place and can be overridden via window.__ENV__ if needed.
 */

const API_CONFIG = {
    baseURL: getAPIBaseURL(),
    apiKey: 'Heart_disease_api',
};

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

    // Production: Railway backend URL
    return 'https://heart-disease-prediction-production-7bb8.up.railway.app';
}
