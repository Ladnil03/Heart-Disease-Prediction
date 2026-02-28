/**
 * ui.js — UI helper utilities
 *
 * Loading overlay, error notifications, and any shared DOM
 * manipulation that doesn't belong in a specific feature module.
 */

// Cached DOM handles (populated in app.js DOMContentLoaded)
let loadingOverlay;

function initUI() {
    loadingOverlay = document.getElementById('loadingOverlay');
    _injectErrorStyles();
    _injectInputErrorStyles();
}

// ---- Loading overlay ----

function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

// ---- Error notifications ----

function showError(message) {
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

    document.body.appendChild(errorDiv);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) errorDiv.remove();
    }, 5000);
}

// ---- Private helpers ----

function _injectErrorStyles() {
    if (document.querySelector('#errorStyles')) return;

    const style = document.createElement('style');
    style.id = 'errorStyles';
    style.textContent = `
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
            to   { transform: translateX(0);    opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

function _injectInputErrorStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .form-group input.error,
        .form-group select.error {
            border-color: #e74c3c;
            box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
        }
    `;
    document.head.appendChild(style);
}
