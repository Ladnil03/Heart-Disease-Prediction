/**
 * chart.js — SHAP feature-importance chart rendering
 *
 * Uses Chart.js to draw a horizontal bar chart of SHAP values
 * and renders the top risk factors as an HTML list.
 */

// Shared labels & interpretations (mirrors backend config.py)
const FACTOR_LABELS = {
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
    thal: 'Thalassemia',
};

const FACTOR_INTERPRETATIONS = {
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
    thal: 'Certain thalassemia types increase risk.',
};

/**
 * Draw a horizontal bar chart of SHAP values on the #shapBarChart canvas.
 */
function renderShapBarChart(shapValues) {
    const ctx = document.getElementById('shapBarChart').getContext('2d');
    const featureNames = Object.keys(shapValues);
    const values = featureNames.map(f => shapValues[f]);
    const barColors = values.map(v => (v >= 0 ? '#e74c3c' : '#27ae60'));

    // Destroy previous chart instance if it exists
    if (window.shapChart) window.shapChart.destroy();

    window.shapChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: featureNames,
            datasets: [{
                label: 'SHAP Value',
                data: values,
                backgroundColor: barColors,
            }],
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: { title: { display: true, text: 'SHAP Value' } },
                y: { title: { display: true, text: 'Feature' } },
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.dataset.label}: ${ctx.parsed.x.toFixed(2)}`,
                    },
                },
            },
        },
    });
}

/**
 * Render a bullet list of the top 3 risk factors with colour-coded
 * effect labels (increasing / decreasing).
 */
function renderTopRiskFactors(topFactors, shapValues) {
    const top3 = topFactors.slice(0, 3);
    let html = '<h5>Top Risk Factors</h5><ul>';

    top3.forEach(f => {
        const label = FACTOR_LABELS[f] || f;
        const interpretation = FACTOR_INTERPRETATIONS[f] || '';
        const shapVal = shapValues[f];
        const effect = shapVal >= 0 ? 'increasing' : 'decreasing';
        const color = effect === 'increasing' ? '#e74c3c' : '#27ae60';
        html += `<li><strong>${label}</strong>: ${interpretation} <span style="color:${color}">(${effect} your risk)</span></li>`;
    });

    html += '</ul>';
    document.getElementById('topRiskFactors').innerHTML = html;
}
