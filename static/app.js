/**
 * Resume AI API - Main Application JavaScript
 * Handles the web interface functionality for bullet generation
 */

// Global variables
let bulletHistory = [];
let selectedHistoryIndex = -1;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadHistory();
    setupEventListeners();
});

// Tab switching functionality
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');

    // Refresh history if switching to history tab
    if (tabName === 'history') {
        loadHistory();
    }
}

// Setup event listeners
function setupEventListeners() {
    const form = document.getElementById('bulletForm');
    form.addEventListener('submit', handleFormSubmit);
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Disable button and show loading
    submitBtn.disabled = true;
    submitText.style.display = 'none';
    loadingSpinner.style.display = 'block';

    try {
        const formData = new FormData(event.target);
        const requestData = {
            accomplished: formData.get('accomplished'),
            measured: formData.get('measured'),
            task: formData.get('task'),
            keyword: formData.get('keyword') || null
        };

        const response = await fetch('/api/v1/bullet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Display results
        displayResults(result.bullet_list);
        
        // Save to history
        saveToHistory(requestData, result.bullet_list);
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('resultsContainer').innerHTML = 
            '<p style="color: #dc3545;">Error generating bullet points. Please try again.</p>';
    } finally {
        // Re-enable button and hide loading
        submitBtn.disabled = false;
        submitText.style.display = 'block';
        loadingSpinner.style.display = 'none';
    }
}

// Display results
function displayResults(bulletList) {
    const container = document.getElementById('resultsContainer');
    
    if (!bulletList || bulletList.length === 0) {
        container.innerHTML = '<p style="color: #666;">No bullet points generated.</p>';
        return;
    }

    const resultsHTML = bulletList.map(item => {
        const scoreClass = getScoreClass(item.score);
        const scorePercentage = Math.round(item.score * 100);
        
        return `
            <div class="bullet-item">
                <div class="bullet-text">${item.bullet}</div>
                <div class="score-container">
                    <span class="score-label">Score:</span>
                    <div class="score-bar">
                        <div class="score-fill ${scoreClass}" style="width: ${scorePercentage}%"></div>
                    </div>
                    <span class="score-value">${item.score.toFixed(2)}</span>
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = resultsHTML;
}

// Get score class for styling
function getScoreClass(score) {
    if (score >= 0.9) return 'excellent';
    if (score >= 0.75) return 'good';
    return 'poor';
}

// Save to localStorage
function saveToHistory(input, output) {
    const historyItem = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        input: input,
        output: output
    };

    bulletHistory.unshift(historyItem);
    
    // Keep only last 50 items
    if (bulletHistory.length > 50) {
        bulletHistory = bulletHistory.slice(0, 50);
    }

    localStorage.setItem('bulletHistory', JSON.stringify(bulletHistory));
}

// Load from localStorage
function loadHistory() {
    const stored = localStorage.getItem('bulletHistory');
    bulletHistory = stored ? JSON.parse(stored) : [];
    displayHistoryList();
}

// Display history list
function displayHistoryList() {
    const container = document.getElementById('historyList');
    
    if (bulletHistory.length === 0) {
        container.innerHTML = '<p style="color: #666; font-style: italic;">No previous bullets found...</p>';
        return;
    }

    const historyHTML = bulletHistory.map((item, index) => {
        const date = new Date(item.timestamp).toLocaleDateString();
        const time = new Date(item.timestamp).toLocaleTimeString();
        const input = item.input.accomplished.substring(0, 50) + (item.input.accomplished.length > 50 ? '...' : '');
        
        return `
            <div class="history-item ${index === selectedHistoryIndex ? 'selected' : ''}" 
                 onclick="selectHistoryItem(${index})">
                <div class="history-input">${input}</div>
                <div class="history-date">${date} at ${time}</div>
            </div>
        `;
    }).join('');

    container.innerHTML = historyHTML;
}

// Select history item
function selectHistoryItem(index) {
    selectedHistoryIndex = index;
    displayHistoryList();
    displayHistoryDetails(bulletHistory[index]);
}

// Display history details
function displayHistoryDetails(item) {
    const container = document.getElementById('historyDetails');
    
    const inputHTML = `
        <div style="margin-bottom: 20px;">
            <h4 style="margin-bottom: 10px; color: #333;">Input:</h4>
            <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <strong>Accomplished:</strong> ${item.input.accomplished}
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <strong>Measured:</strong> ${item.input.measured}
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <strong>Task:</strong> ${item.input.task}
            </div>
            ${item.input.keyword ? `<div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <strong>Keyword:</strong> ${item.input.keyword}
            </div>` : ''}
        </div>
    `;

    const outputHTML = `
        <div>
            <h4 style="margin-bottom: 10px; color: #333;">Generated Bullets:</h4>
            ${item.output.map(bulletItem => {
                const scoreClass = getScoreClass(bulletItem.score);
                const scorePercentage = Math.round(bulletItem.score * 100);
                
                return `
                    <div class="bullet-item">
                        <div class="bullet-text">${bulletItem.bullet}</div>
                        <div class="score-container">
                            <span class="score-label">Score:</span>
                            <div class="score-bar">
                                <div class="score-fill ${scoreClass}" style="width: ${scorePercentage}%"></div>
                            </div>
                            <span class="score-value">${bulletItem.score.toFixed(2)}</span>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;

    container.innerHTML = inputHTML + outputHTML;
}

// Clear history
function clearHistory() {
    if (confirm('Are you sure you want to clear all history?')) {
        bulletHistory = [];
        localStorage.removeItem('bulletHistory');
        selectedHistoryIndex = -1;
        displayHistoryList();
        document.getElementById('historyDetails').innerHTML = 
            '<div class="no-selection">Select a bullet from the list to view details</div>';
    }
} 