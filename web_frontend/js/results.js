/**
 * results.js — Prediction result display & report download
 *
 * Builds the result HTML, shows/hides the SHAP section, and wires
 * up the PDF download button.
 */

// ---- Risk-level helper look-ups ----

const RISK_ICONS = {
    Low: 'check-circle',
    Moderate: 'exclamation-triangle',
    High: 'exclamation-circle',
};

const RISK_COLORS = {
    Low: '#27ae60',
    Moderate: '#f39c12',
    High: '#e74c3c',
};

const RISK_RECOMMENDATIONS = {
    Low: 'Maintain healthy lifestyle habits',
    Moderate: 'Consider consulting a healthcare provider',
    High: 'Seek immediate medical attention',
};

function getRiskIcon(level) { return RISK_ICONS[level] || 'question-circle'; }
function getRiskColor(level) { return RISK_COLORS[level] || '#95a5a6'; }
function getRecommendation(level) { return RISK_RECOMMENDATIONS[level] || 'Consult with a healthcare professional'; }

/**
 * Render the full prediction result into #resultContent and reveal the
 * result section.
 */
function displayResults(result) {
    const { risk_probability, risk_level, shap_values, top_risk_factors, base_value } = result;

    const resultContent = document.getElementById('resultContent');
    const resultSection = document.getElementById('resultSection');

    resultContent.innerHTML = `
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

    resultSection.classList.remove('hidden');

    // SHAP Feature Importance
    const featureSection = document.getElementById('featureImportanceSection');
    const downloadBtn = document.getElementById('downloadReportBtn');

    if (shap_values && typeof shap_values === 'object') {
        renderShapBarChart(shap_values);
        renderTopRiskFactors(top_risk_factors, shap_values);
        featureSection.classList.remove('hidden');
        downloadBtn.classList.remove('hidden');
        setupDownloadReportBtn(result);
    } else {
        featureSection.classList.add('hidden');
        downloadBtn.classList.add('hidden');
    }

    resultSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Attach the click handler for the PDF download button.
 */
function setupDownloadReportBtn(result) {
    const btn = document.getElementById('downloadReportBtn');
    const form = document.getElementById('predictionForm');

    btn.onclick = async () => {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating Report...';

        try {
            const formData = collectFormData(form);
            const payload = {
                ...formData,
                risk_probability: result.risk_probability,
                risk_level: result.risk_level,
                shap_values: result.shap_values,
                top_risk_factors: result.top_risk_factors,
                base_value: result.base_value,
            };
            await downloadReport(payload);
        } catch (err) {
            showError('PDF report generation failed.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-file-download"></i> Download Report (PDF)';
        }
    };
}
