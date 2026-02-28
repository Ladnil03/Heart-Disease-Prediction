// Configuration - supports both local and production deployments
const API_CONFIG = {
    baseURL: getAPIBaseURL(),
    apiKey: 'Heart_disease_api'
};

// Determine API base URL based on environment
function getAPIBaseURL() {
    // Local development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:8000';
    }

    // Production: Railway backend URL
    return 'https://heart-disease-prediction-production-7bb8.up.railway.app';
}

// DOM Elements
const form = document.getElementById('predictionForm');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultSection = document.getElementById('resultSection');
const resultContent = document.getElementById('resultContent');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    try {
        // Show loading
        showLoading();

        // Collect form data
        const formData = collectFormData();

        // Validate form data
        if (!validateFormData(formData)) {
            hideLoading();
            return;
        }

        // Make API call
        const result = await makePrediction(formData);

        // Display results
        displayResults(result);

    } catch (error) {
        console.error('Prediction error:', error);
        showError(error.message);
    } finally {
        hideLoading();
    }
});

// Collect form data
function collectFormData() {
    const formData = new FormData(form);
    const data = {};

    // Convert form data to object with proper types
    for (let [key, value] of formData.entries()) {
        if (key === 'oldpeak') {
            data[key] = parseFloat(value);
        } else {
            data[key] = parseInt(value);
        }
    }

    return data;
}

// Validate form data
function validateFormData(data) {
    const validations = {
        age: { min: 1, max: 150 },
        sex: { min: 0, max: 1 },
        cp: { min: 0, max: 3 },
        trestbps: { min: 50, max: 300 },
        chol: { min: 100, max: 600 },
        fbs: { min: 0, max: 1 },
        restecg: { min: 0, max: 2 },
        thalach: { min: 60, max: 250 },
        exang: { min: 0, max: 1 },
        oldpeak: { min: 0.0, max: 10.0 },
        slope: { min: 0, max: 2 },
        ca: { min: 0, max: 3 },
        thal: { min: 1, max: 3 }
    };

    for (let [field, rules] of Object.entries(validations)) {
        const value = data[field];
        if (value < rules.min || value > rules.max) {
            showError(`${field} must be between ${rules.min} and ${rules.max}`);
            return false;
        }
    }

    return true;
}

// Make prediction API call
async function makePrediction(data) {
    const response = await fetch(`${API_CONFIG.baseURL}/api/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api-key': API_CONFIG.apiKey
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
}

// Display prediction results
function displayResults(result) {
    const { risk_probability, risk_level, shap_values, top_risk_factors, base_value } = result;

    // Create result HTML
    const resultHTML = `
        <div class="risk-level risk-${risk_level.toLowerCase()}">
            <div>
                <i class="fas fa-${getRiskIcon(risk_level)}"></i>
                <h4>Risk Level: ${risk_level}</h4>
                <p>Based on the provided medical parameters</p>
            </div>
        </div>
        <div class="risk-probability">
            <div class="probability-circle" style="background: conic-gradient(from 0deg, ${getRiskColor(risk_level)} ${risk_probability * 360}deg, #e8f0fe ${risk_probability * 360}deg)">
                <div class="percent-value">
                    <span>${Math.round(risk_probability * 100)}%</span>
                    <small>RISK</small>
                </div>
            </div>
            <div class="probability-text">
                <strong>Risk Probability</strong><br>
                <span style="color: var(--text-gray); font-size: 0.95rem;">${getRecommendation(risk_level)}</span>
            </div>
        </div>
    `;

    resultContent.innerHTML = resultHTML;
    resultSection.classList.remove('hidden');

    // SHAP Feature Importance
    if (shap_values && typeof shap_values === 'object') {
        renderShapBarChart(shap_values);
        renderTopRiskFactors(top_risk_factors, shap_values);
        document.getElementById('featureImportanceSection').classList.remove('hidden');
        // Show Download Report button
        document.getElementById('downloadReportBtn').classList.remove('hidden');
        // Attach handler for PDF download
        setupDownloadReportBtn(result);
    } else {
        document.getElementById('featureImportanceSection').classList.add('hidden');
        document.getElementById('downloadReportBtn').classList.add('hidden');
    }

    // Smooth scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Setup Download Report button handler
function setupDownloadReportBtn(result) {
    const btn = document.getElementById('downloadReportBtn');
    btn.onclick = async function () {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating Report...';
        try {
            // Collect form data again for full input
            const formData = collectFormData();
            // Build report payload
            const payload = {
                ...formData,
                risk_probability: result.risk_probability,
                risk_level: result.risk_level,
                shap_values: result.shap_values,
                top_risk_factors: result.top_risk_factors,
                base_value: result.base_value
            };
            const response = await fetch(`${API_CONFIG.baseURL}/api/report`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'api-key': API_CONFIG.apiKey
                },
                body: JSON.stringify(payload)
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
        } catch (err) {
            showError('PDF report generation failed.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-file-download"></i> Download Report (PDF)';
        }
    };
}

// Render SHAP bar chart
function renderShapBarChart(shapValues) {
    const ctx = document.getElementById('shapBarChart').getContext('2d');
    const featureNames = Object.keys(shapValues);
    const values = featureNames.map(f => shapValues[f]);
    const barColors = values.map(v => v >= 0 ? '#e74c3c' : '#27ae60'); // Red for risk-increasing, green for decreasing

    // Destroy previous chart if exists
    if (window.shapChart) window.shapChart.destroy();

    window.shapChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: featureNames,
            datasets: [{
                label: 'SHAP Value',
                data: values,
                backgroundColor: barColors
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    title: { display: true, text: 'SHAP Value' }
                },
                y: {
                    title: { display: true, text: 'Feature' }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.parsed.x.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

// Render top risk factors explanations
function renderTopRiskFactors(topFactors, shapValues) {
    const factorLabels = {
        age: 'Your Age',
        sex: 'Sex',
        cp: 'Chest Pain Type',
        trestbps: 'Resting Blood Pressure',
        chol: 'Cholesterol Level',
        fbs: 'Fasting Blood Sugar',
        restecg: 'Resting ECG',
        thalach: 'Maximum Heart Rate',
        exang: 'Exercise Induced Angina',
        oldpeak: 'ST Depression',
        slope: 'ST Segment Slope',
        ca: 'Major Vessels',
        thal: 'Thalassemia'
    };
    const interpretations = {
        age: 'Older age increases risk.',
        sex: 'Male sex increases risk.',
        cp: 'Certain chest pain types increase risk.',
        trestbps: 'Higher resting blood pressure increases risk.',
        chol: 'Higher cholesterol increases risk.',
        fbs: 'High fasting blood sugar increases risk.',
        restecg: 'Abnormal ECG increases risk.',
        thalach: 'Lower maximum heart rate increases risk.',
        exang: 'Exercise-induced angina increases risk.',
        oldpeak: 'Greater ST depression increases risk.',
        slope: 'Flat or downsloping ST segment increases risk.',
        ca: 'More major vessels increases risk.',
        thal: 'Certain thalassemia types increase risk.'
    };
    const top3 = topFactors.slice(0, 3);
    let html = '<h5>Top Risk Factors</h5><ul>';
    top3.forEach(f => {
        const label = factorLabels[f] || f;
        const interpretation = interpretations[f] || '';
        const shapVal = shapValues[f];
        const effect = shapVal >= 0 ? 'increasing' : 'decreasing';
        html += `<li><strong>${label}</strong>: ${interpretation} <span style="color:${effect === 'increasing' ? '#e74c3c' : '#27ae60'}">(${effect} your risk)</span></li>`;
    });
    html += '</ul>';
    document.getElementById('topRiskFactors').innerHTML = html;
}

// Get risk icon based on level
function getRiskIcon(riskLevel) {
    const icons = {
        'Low': 'check-circle',
        'Moderate': 'exclamation-triangle',
        'High': 'exclamation-circle'
    };
    return icons[riskLevel] || 'question-circle';
}

// Get risk color based on level
function getRiskColor(riskLevel) {
    const colors = {
        'Low': '#27ae60',
        'Moderate': '#f39c12',
        'High': '#e74c3c'
    };
    return colors[riskLevel] || '#95a5a6';
}

// Get recommendation based on risk level
function getRecommendation(riskLevel) {
    const recommendations = {
        'Low': 'Maintain healthy lifestyle habits',
        'Moderate': 'Consider consulting a healthcare provider',
        'High': 'Seek immediate medical attention'
    };
    return recommendations[riskLevel] || 'Consult with a healthcare professional';
}

// Show loading overlay
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

// Show error message
function showError(message) {
    // Create error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <div class="error-content">
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Add error styles if not already added
    if (!document.querySelector('#errorStyles')) {
        const errorStyles = document.createElement('style');
        errorStyles.id = 'errorStyles';
        errorStyles.textContent = `
            .error-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: #e74c3c;
                color: white;
                padding: 15px 20px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(231, 76, 60, 0.3);
                z-index: 1001;
                animation: slideIn 0.3s ease;
            }
            
            .error-content {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .error-content button {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                font-size: 1.1rem;
                padding: 0;
                margin-left: 10px;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(errorStyles);
    }

    document.body.appendChild(errorDiv);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

// Form validation on input change
document.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('change', function () {
        // Remove any existing error styling
        this.classList.remove('error');

        // Basic validation
        if (this.hasAttribute('required') && !this.value) {
            this.classList.add('error');
        }
    });
});

// Add error styling for invalid inputs
const errorInputStyles = document.createElement('style');
errorInputStyles.textContent = `
    .form-group input.error,
    .form-group select.error {
        border-color: #e74c3c;
        box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
    }
`;
document.head.appendChild(errorInputStyles);

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    console.log('Heart Disease Prediction App Initialized');

    // Hide result section initially
    resultSection.classList.add('hidden');

    // Test API connection on page load
    testAPIConnection();
});

// Test API connection
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_CONFIG.baseURL}/`, {
            method: 'GET'
        });
        console.log('API connection test completed');
    } catch (error) {
        console.warn('API connection test failed:', error.message);
    }
}