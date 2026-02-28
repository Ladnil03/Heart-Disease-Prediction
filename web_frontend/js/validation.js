/**
 * validation.js — Form data collection & validation
 *
 * All field-level validation rules live here so changes to
 * accepted ranges only need to happen in one place (mirroring
 * the Pydantic schema on the backend).
 */

const VALIDATION_RULES = {
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
    thal: { min: 1, max: 3 },
};

/**
 * Collect form data from the prediction form and cast to
 * the correct numeric types.
 */
function collectFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};

    for (const [key, value] of formData.entries()) {
        data[key] = key === 'oldpeak' ? parseFloat(value) : parseInt(value, 10);
    }

    return data;
}

/**
 * Validate the collected form data object against VALIDATION_RULES.
 * Returns true if valid; shows an error notification and returns false otherwise.
 */
function validateFormData(data) {
    for (const [field, rules] of Object.entries(VALIDATION_RULES)) {
        const value = data[field];
        if (value < rules.min || value > rules.max) {
            showError(`${field} must be between ${rules.min} and ${rules.max}`);
            return false;
        }
    }
    return true;
}
