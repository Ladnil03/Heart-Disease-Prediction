/**
 * api.js — API communication layer
 *
 * All fetch calls to the backend are routed through this module.
 * Adding auth headers, error handling, and base URL resolution
 * happens in one place.
 */

/**
 * Send patient data to the prediction endpoint and return the
 * parsed JSON result.
 * @param {Object} data – collected form data
 * @returns {Promise<Object>} prediction result
 */
async function makePrediction(data) {
    const response = await fetch(`${API_CONFIG.baseURL}/api/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api-key': API_CONFIG.apiKey,
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Request a PDF report from the backend and trigger a browser download.
 * @param {Object} payload – report data (form data + prediction result)
 */
async function downloadReport(payload) {
    const response = await fetch(`${API_CONFIG.baseURL}/api/report`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api-key': API_CONFIG.apiKey,
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error('Failed to generate PDF report');

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Heart_Disease_Report.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}

/**
 * Simple health-check / connectivity test against the root endpoint.
 */
async function testAPIConnection() {
    try {
        await fetch(`${API_CONFIG.baseURL}/`, { method: 'GET' });
        console.log('API connection test completed');
    } catch (error) {
        console.warn('API connection test failed:', error.message);
    }
}
