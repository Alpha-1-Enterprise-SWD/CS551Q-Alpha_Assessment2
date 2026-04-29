// Practice Detail Page JavaScript

// Load age distribution chart
function loadAgeDistributionChart() {
    const ctx = document.getElementById('ageDistributionChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ageGroups,
            datasets: [
                {
                    label: 'Male',
                    data: maleAges,
                    backgroundColor: '#0d6efd',
                    borderColor: '#0a58ca',
                    borderWidth: 1
                },
                {
                    label: 'Female',
                    data: femaleAges,
                    backgroundColor: '#d63384',
                    borderColor: '#c22550',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true,
                    ticks: {
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.dataset.label + ': ' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Load gender distribution chart
function loadGenderDistributionChart() {
    const ctx = document.getElementById('genderDistributionChart');
    if (!ctx) return;

    // Calculate totals
    const totalMale = maleAges.reduce((a, b) => a + b, 0);
    const totalFemale = femaleAges.reduce((a, b) => a + b, 0);
    const total = totalMale + totalFemale;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Male', 'Female'],
            datasets: [{
                data: [totalMale, totalFemale],
                backgroundColor: ['#0d6efd', '#d63384'],
                borderColor: ['#fff', '#fff'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value.toLocaleString()} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Export practice data
function exportPracticeData() {
    // Create data object
    const practiceData = {
        practice_name: document.querySelector('h2').textContent.trim(),
        practice_code: '{{ practice.practice_code }}',
        address: '{{ practice.address }}',
        postcode: '{{ practice.postcode }}',
        telephone: '{{ practice.telephone }}',
        health_board: '{{ practice.health_board }}',
        total_patients: {{ practice.list_size }
},
gp_count: { { gp_count } },
patient_to_gp_ratio: { { patient_to_gp_ratio } },
age_groups: ageGroups.map((age, index) => ({
    age_group: age,
    male: maleAges[index],
    female: femaleAges[index],
    total: maleAges[index] + femaleAges[index]
}))
    };

// Convert to CSV
const csvContent = convertToCSV(practiceData);

// Create download link
const blob = new Blob([csvContent], { type: 'text/csv' });
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `${practiceData.practice_name.replace(/[^a-z0-9]/gi, '_')}_data.csv`;
document.body.appendChild(a);
a.click();
document.body.removeChild(a);
window.URL.revokeObjectURL(url);
}

// Convert data to CSV format
function convertToCSV(data) {
    let csv = 'Practice Data Export\n\n';
    csv += `Practice Name,${data.practice_name}\n`;
    csv += `Practice Code,${data.practice_code}\n`;
    csv += `Address,${data.address}\n`;
    csv += `Postcode,${data.postcode}\n`;
    csv += `Telephone,${data.telephone}\n`;
    csv += `Health Board,${data.health_board}\n`;
    csv += `Total Patients,${data.total_patients}\n`;
    csv += `GP Count,${data.gp_count}\n`;
    csv += `Patient/GP Ratio,${data.patient_to_gp_ratio}\n\n`;

    csv += 'Age Group Distribution\n';
    csv += 'Age Group,Male,Female,Total,Percentage\n';

    const totalPatients = data.total_patients;
    data.age_groups.forEach(age => {
        const percentage = totalPatients > 0 ? ((age.total / totalPatients) * 100).toFixed(2) : 0;
        csv += `${age.age_group},${age.male},${age.female},${age.total},${percentage}%\n`;
    });

    return csv;
}

// Print report with enhanced formatting
function printReport() {
    // Add print-specific styles
    const printStyles = document.createElement('style');
    printStyles.textContent = `
        @media print {
            body { font-size: 10pt; }
            .card { border: 1px solid #000; page-break-inside: avoid; }
            .no-print { display: none !important; }
            .table { font-size: 9pt; }
            h2 { font-size: 16pt; }
            h3 { font-size: 14pt; }
        }
    `;
    document.head.appendChild(printStyles);

    // Trigger print dialog
    window.print();

    // Remove print styles after printing
    setTimeout(() => {
        document.head.removeChild(printStyles);
    }, 1000);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add keyboard shortcuts
    setupKeyboardShortcuts();
});

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function (e) {
        // Ctrl/Cmd + P: Print
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            printReport();
        }

        // Ctrl/Cmd + E: Export
        if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
            e.preventDefault();
            exportPracticeData();
        }

        // Ctrl/Cmd + B: Go back
        if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
            e.preventDefault();
            window.history.back();
        }
    });
}

// Animate statistics on page load
function animateStatistics() {
    const statElements = document.querySelectorAll('.card-body h4');

    statElements.forEach(element => {
        const targetValue = parseInt(element.textContent.replace(/,/g, ''));
        if (!isNaN(targetValue)) {
            animateValue(element, 0, targetValue, 1000);
        }
    });
}

// Animate numeric values
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            element.textContent = end.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Add smooth scroll behavior
function addSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize page enhancements
document.addEventListener('DOMContentLoaded', function () {
    animateStatistics();
    addSmoothScroll();

    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            if (!this.disabled) {
                const originalContent = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                this.disabled = true;

                // Reset after 2 seconds (in case of error)
                setTimeout(() => {
                    this.innerHTML = originalContent;
                    this.disabled = false;
                }, 2000);
            }
        });
    });
});

// Error handling for charts
window.addEventListener('error', function (e) {
    if (e.target.tagName === 'CANVAS') {
        console.error('Chart loading error:', e.error);
        // Show fallback message
        const canvas = e.target;
        const container = canvas.parentElement;
        container.innerHTML = '<div class="alert alert-warning">Chart could not be loaded. Please refresh the page.</div>';
    }
});

// Performance monitoring
window.addEventListener('load', function () {
    const loadTime = performance.now();
    console.log(`Practice detail page loaded in ${loadTime.toFixed(2)}ms`);
});