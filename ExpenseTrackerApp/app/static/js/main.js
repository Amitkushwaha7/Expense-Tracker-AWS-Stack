// Main JavaScript file for the Expense Tracker application

document.addEventListener('DOMContentLoaded', function() {
    // Automatically close alert messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Format currency inputs
    // Charts (initialized if canvases present)
    const expenseCanvas = document.getElementById('expenseChart');
    if (expenseCanvas && expenseCanvas.dataset.categories) {
        try {
            const catData = JSON.parse(expenseCanvas.dataset.categories);
            const labels = Object.keys(catData).map(cat => cat.charAt(0).toUpperCase() + cat.slice(1));
            const values = Object.values(catData);
            new Chart(expenseCanvas, {
                type: 'doughnut',
                data: {
                    labels,
                    datasets: [{
                        data: values,
                        backgroundColor: ['#4e73df','#1cc88a','#36b9cc','#f6c23e','#e74a3b','#fd7e14','#6f42c1','#20c9a6','#5a5c69','#858796']
                    }]
                },
                options: { maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
            });
        } catch (e) { console.warn('Failed to render category chart', e); }
    }

    const trendCanvas = document.getElementById('trendChart');
    if (trendCanvas && trendCanvas.dataset.labels && trendCanvas.dataset.values) {
        try {
            const labels = JSON.parse(trendCanvas.dataset.labels);
            const values = JSON.parse(trendCanvas.dataset.values);
            new Chart(trendCanvas, {
                type: 'line',
                data: { labels, datasets: [{ label: 'Spent', data: values, borderColor: '#0d6efd', backgroundColor: 'rgba(13,110,253,.15)', fill: true, tension: .3 }]},
                options: { maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
            });
        } catch (e) { console.warn('Failed to render trend chart', e); }
    }

    const amountInputs = document.querySelectorAll('input[name="amount"]');
    amountInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                const value = parseFloat(this.value);
                if (!isNaN(value)) {
                    this.value = value.toFixed(2);
                }
            }
        });
    });

    // Confirm deletion of expenses
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this expense?')) {
                e.preventDefault();
            }
        });
    });

    // Budget warning when value is over 80% of budget
    const budgetRemaining = document.querySelector('.budget-remaining');
    if (budgetRemaining) {
        const budgetValue = parseFloat(budgetRemaining.dataset.value || 0);
        const totalBudget = parseFloat(budgetRemaining.dataset.total || 0);
        
        if (totalBudget > 0 && budgetValue < totalBudget * 0.2) {
            budgetRemaining.classList.add('text-danger', 'fw-bold');
        }
    }

    // Apply progress bar styling/width from data attributes
    document.querySelectorAll('.progress-bar[data-progress-class]').forEach(function(bar) {
        const cls = bar.getAttribute('data-progress-class');
        if (cls) bar.classList.add(cls);
        const width = bar.getAttribute('data-width');
        if (width) bar.style.width = `${width}%`;
    });

    // Apply alert classes from data-category to avoid jinja in class attribute
    document.querySelectorAll('.alert[data-category]').forEach(function(alert) {
        const cat = alert.getAttribute('data-category');
        const bsClass = cat && cat !== 'message' ? `alert-${cat}` : 'alert-info';
        alert.classList.add(bsClass);
    });

    // Apply category color badges from data-color
    document.querySelectorAll('.cat-color[data-color]').forEach(function(el) {
        const color = el.getAttribute('data-color');
        if (color) {
            el.style.backgroundColor = color;
            el.style.color = '#111';
        }
    });

    // Fixed theme (no toggle) – use dark to match design
    document.documentElement.setAttribute('data-bs-theme', 'dark');

    // Enable tooltips on any elements using data-bs-toggle="tooltip"
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl)
    })
});
