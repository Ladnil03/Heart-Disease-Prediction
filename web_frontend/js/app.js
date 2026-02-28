/**
 * app.js — Main application entry point
 *
 * Wires up event listeners and initialises the page.
 * All logic is delegated to the other modules (config, validation,
 * api, ui, chart, results).
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Heart Disease Prediction App Initialized');

    // Initialise UI helpers (caches DOM refs, injects styles)
    initUI();

    const form = document.getElementById('predictionForm');
    const resultSection = document.getElementById('resultSection');

    // Ensure result section starts hidden
    resultSection.classList.add('hidden');

    // ---- Form submission ----
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        try {
            showLoading();

            const formData = collectFormData(form);

            if (!validateFormData(formData)) {
                hideLoading();
                return;
            }

            const result = await makePrediction(formData);
            displayResults(result);
        } catch (error) {
            console.error('Prediction error:', error);
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    // ---- Live input validation ----
    document.querySelectorAll('input, select').forEach(input => {
        input.addEventListener('change', function () {
            this.classList.remove('error');
            if (this.hasAttribute('required') && !this.value) {
                this.classList.add('error');
            }
        });
    });

    // ---- Test backend connectivity ----
    testAPIConnection();
});
