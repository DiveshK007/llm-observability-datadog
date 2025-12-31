/**
 * LLM Observability - Frontend JavaScript
 * Handles API interactions and UI updates
 */

// Configuration
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : window.location.origin;

// DOM Elements
const queryForm = document.getElementById('queryForm');
const promptInput = document.getElementById('prompt');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoader = submitBtn.querySelector('.btn-loader');
const responseSection = document.getElementById('responseSection');
const responseContent = document.getElementById('responseContent');
const metricLatency = document.getElementById('metricLatency');
const metricTokens = document.getElementById('metricTokens');
const metricCost = document.getElementById('metricCost');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const dismissError = document.getElementById('dismissError');

/**
 * Show loading state
 */
function setLoading(loading) {
    submitBtn.disabled = loading;
    btnText.hidden = loading;
    btnLoader.hidden = !loading;
    promptInput.disabled = loading;
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.hidden = false;
    responseSection.hidden = true;
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.hidden = true;
}

/**
 * Show response with metrics
 */
function showResponse(data) {
    // Update metrics
    metricLatency.textContent = `${Math.round(data.latency_ms)} ms`;
    metricTokens.textContent = data.tokens_used.toLocaleString();
    metricCost.textContent = `$${data.estimated_cost_usd.toFixed(6)}`;

    // Update response content
    responseContent.textContent = data.response;

    // Show response section
    responseSection.hidden = false;
    errorSection.hidden = true;
}

/**
 * Submit query to API
 */
async function submitQuery(prompt) {
    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                max_tokens: 1024
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Unable to connect to API. Please ensure the server is running.');
        }
        throw error;
    }
}

/**
 * Handle form submission
 */
async function handleSubmit(event) {
    event.preventDefault();

    const prompt = promptInput.value.trim();
    if (!prompt) return;

    setLoading(true);
    hideError();

    try {
        const data = await submitQuery(prompt);
        showResponse(data);
    } catch (error) {
        console.error('Query failed:', error);
        showError(error.message || 'An unexpected error occurred');
    } finally {
        setLoading(false);
    }
}

/**
 * Initialize event listeners
 */
function init() {
    queryForm.addEventListener('submit', handleSubmit);
    dismissError.addEventListener('click', hideError);

    // Auto-resize textarea
    promptInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 300) + 'px';
    });

    // Keyboard shortcut: Cmd/Ctrl + Enter to submit
    promptInput.addEventListener('keydown', function (e) {
        if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
            handleSubmit(e);
        }
    });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);
