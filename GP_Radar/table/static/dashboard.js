// Dashboard JavaScript for GP Radar

let map = null;
let markers = [];

// Initialize dashboard
function initializeDashboard() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Setup postcode search
    setupPostcodeSearch();
}

// Setup postcode search
function setupPostcodeSearch() {
    const postcodeInput = document.getElementById('postcode_search');
    if (postcodeInput) {
        let searchTimeout;
        postcodeInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 500ms delay
                if (postcodeInput.value.length >= 2 || postcodeInput.value.length === 0) {
                    document.getElementById('postcodeSearchForm').submit();
                }
            }, 500);
        });

        // Handle form submission
        document.getElementById('postcodeSearchForm').addEventListener('submit', function (e) {
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Searching...';
            submitBtn.disabled = true;

            // Reset button after 2 seconds (in case of slow response)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
}

// Clear postcode search
function clearPostcodeSearch() {
    const postcodeInput = document.getElementById('postcode_search');
    if (postcodeInput) {
        postcodeInput.value = '';
        document.getElementById('postcodeSearchForm').submit();
    }
}

// Toggle between table and card view
function toggleView(viewType) {
    const tableView = document.getElementById('tableView');
    const cardView = document.getElementById('cardView');

    if (viewType === 'table') {
        tableView.style.display = 'block';
        cardView.style.display = 'none';
    } else if (viewType === 'cards') {
        tableView.style.display = 'none';
        cardView.style.display = 'block';
    }
}

// Change page size and reload the page
function changePageSize() {
    const pageSize = document.getElementById('pageSize').value;
    const currentUrl = new URL(window.location);

    // Update or add page_size parameter
    currentUrl.searchParams.set('page_size', pageSize);

    // Reset to page 1 when changing page size
    currentUrl.searchParams.set('page', '1');

    // Reload the page with new parameters
    window.location.href = currentUrl.toString();
}

// Toggle GP list expansion
function toggleGPList(element) {
    const targetId = element.getAttribute('data-target');
    const gpList = document.getElementById(targetId);
    const icon = element.querySelector('i');
    const toggleText = element.querySelector('.toggle-text');

    if (!gpList) return;

    const hiddenItems = gpList.querySelectorAll('.gp-item[style*="display: none"]');
    const visibleItems = gpList.querySelectorAll('.gp-item[style*="display: block"]');

    if (hiddenItems.length > 0) {
        // Show all items
        gpList.querySelectorAll('.gp-item').forEach(item => {
            item.style.display = 'block';
        });

        // Update UI to show collapse state
        icon.className = 'fas fa-minus-circle me-1';
        toggleText.textContent = 'Show less';
    } else {
        // Hide items beyond the first 3
        const allItems = gpList.querySelectorAll('.gp-item');
        allItems.forEach((item, index) => {
            if (index >= 3) {
                item.style.display = 'none';
            }
        });

        // Update UI to show expand state
        icon.className = 'fas fa-plus-circle me-1';
        const hiddenCount = allItems.length - 3;
        toggleText.textContent = `Show ${hiddenCount} more GP${hiddenCount !== 1 ? 's' : ''}`;
    }
}

// Load health board distribution chart
function loadHealthBoardChart() {
    const ctx = document.getElementById('healthBoardChart');
    if (!ctx) return;

    // Get health board data from the page
    const healthBoardData = getHealthBoardData();

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: healthBoardData.labels,
            datasets: [{
                data: healthBoardData.data,
                backgroundColor: [
                    '#0d6efd',
                    '#198754',
                    '#fd7e14',
                    '#dc3545',
                    '#6f42c1',
                    '#20c997',
                    '#ffc107',
                    '#6c757d'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Load patient to GP ratio chart
function loadRatioChart() {
    const ctx = document.getElementById('ratioChart');
    if (!ctx) return;

    const ratioData = getRatioData();

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ratioData.labels,
            datasets: [{
                label: 'Patient/GP Ratio',
                data: ratioData.data,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Ratio: ${context.parsed.y.toFixed(1)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Patients per GP'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Practice'
                    }
                }
            }
        }
    });
}

// Load practice size distribution chart
function loadSizeChart() {
    const ctx = document.getElementById('sizeChart');
    if (!ctx) return;

    const sizeData = getSizeData();

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sizeData.labels,
            datasets: [{
                label: 'Patient List Size',
                data: sizeData.data,
                backgroundColor: [
                    '#198754',
                    '#20c997',
                    '#0d6efd',
                    '#6f42c1',
                    '#fd7e14'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Patients: ${context.parsed.y.toLocaleString()}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Patients'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Practice Size Range'
                    }
                }
            }
        }
    });
}

// Get health board data from the current page
function getHealthBoardData() {
    const healthBoards = {};
    const rows = document.querySelectorAll('#tableView tbody tr');

    rows.forEach(row => {
        const badge = row.querySelector('.badge');
        if (badge) {
            const boardName = badge.textContent.trim();
            healthBoards[boardName] = (healthBoards[boardName] || 0) + 1;
        }
    });

    // Limit to top 8 boards for better visualization
    const sortedBoards = Object.entries(healthBoards)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 8);

    return {
        labels: sortedBoards.map(([name]) => name),
        data: sortedBoards.map(([, count]) => count)
    };
}

// Get patient to GP ratio data
function getRatioData() {
    const rows = document.querySelectorAll('#tableView tbody tr');
    const ratios = [];

    rows.forEach((row, index) => {
        const ratioCell = row.cells[5]; // Patient/GP Ratio column
        if (ratioCell) {
            const ratioText = ratioCell.textContent.trim();
            const ratio = parseFloat(ratioText.replace(',', ''));
            if (!isNaN(ratio)) {
                ratios.push({
                    practice: row.querySelector('strong').textContent,
                    ratio: ratio
                });
            }
        }
    });

    // Sort by practice name and take first 10 for visualization
    ratios.sort((a, b) => a.practice.localeCompare(b.practice));
    const topRatios = ratios.slice(0, 10);

    return {
        labels: topRatios.map(r => r.practice.length > 15 ? r.practice.substring(0, 15) + '...' : r.practice),
        data: topRatios.map(r => r.ratio)
    };
}

// Get practice size distribution data
function getSizeData() {
    const rows = document.querySelectorAll('#tableView tbody tr');
    const sizes = [];

    rows.forEach(row => {
        const sizeCell = row.cells[3]; // Total Patients column
        if (sizeCell) {
            const sizeText = sizeCell.querySelector('strong').textContent.trim();
            const size = parseInt(sizeText.replace(',', ''));
            if (!isNaN(size)) {
                sizes.push(size);
            }
        }
    });

    // Group practices by size ranges
    const ranges = {
        '0-1000': 0,
        '1001-2500': 0,
        '2501-5000': 0,
        '5001-10000': 0,
        '10000+': 0
    };

    sizes.forEach(size => {
        if (size <= 1000) ranges['0-1000']++;
        else if (size <= 2500) ranges['1001-2500']++;
        else if (size <= 5000) ranges['2501-5000']++;
        else if (size <= 10000) ranges['5001-10000']++;
        else ranges['10000+']++;
    });

    return {
        labels: Object.keys(ranges),
        data: Object.values(ranges)
    };
}

// Initialize map
function initializeMap() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    // Initialize Leaflet map centered on Scotland
    map = L.map('map').setView([56.4907, -4.2026], 6);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add practice markers
    addPracticeMarkers();
}

// Add practice markers to map
function addPracticeMarkers() {
    if (!map) return;

    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Get practice data from the table
    const rows = document.querySelectorAll('#tableView tbody tr');

    rows.forEach((row, index) => {
        const practiceName = row.querySelector('strong').textContent;
        const address = row.querySelector('.text-muted').textContent;
        const patientCount = row.cells[2].textContent.trim();
        const gpCount = row.cells[3].textContent.trim();
        const ratio = row.cells[4].textContent.trim();

        // Create popup content
        const popupContent = `
            <div style="min-width: 200px;">
                <h6>${practiceName}</h6>
                <p class="mb-1"><small>${address}</small></p>
                <div class="row text-center">
                    <div class="col-4">
                        <strong>${patientCount}</strong><br>
                        <small>Patients</small>
                    </div>
                    <div class="col-4">
                        <strong>${gpCount}</strong><br>
                        <small>GPs</small>
                    </div>
                    <div class="col-4">
                        <strong>${ratio}</strong><br>
                        <small>Ratio</small>
                    </div>
                </div>
            </div>
        `;

        // Create marker (using approximate coordinates for demonstration)
        // In a real implementation, you'd use actual latitude/longitude from the database
        const lat = 56.4907 + (Math.random() - 0.5) * 2;
        const lng = -4.2026 + (Math.random() - 0.5) * 4;

        const marker = L.marker([lat, lng])
            .bindPopup(popupContent)
            .addTo(map);

        markers.push(marker);
    });
}

// Show practice on map
function showOnMap(latitude, longitude) {
    if (!map) {
        initializeMap();
        return;
    }

    if (latitude && longitude) {
        map.setView([latitude, longitude], 10);

        // Find and open the marker popup
        markers.forEach(marker => {
            const pos = marker.getLatLng();
            if (Math.abs(pos.lat - latitude) < 0.001 && Math.abs(pos.lng - longitude) < 0.001) {
                marker.openPopup();
            }
        });
    } else {
        // If no coordinates, show a message
        alert('Location coordinates not available for this practice.');
    }
}

// Export data
function exportData() {
    // Get current filter parameters
    const urlParams = new URLSearchParams(window.location.search);

    // Create export URL (this would be implemented as a Django view)
    const exportUrl = `{% url 'export_data' %}?${urlParams.toString()}`;

    // For now, just show a message
    alert('Export functionality would download filtered data as CSV/Excel file');

    // In a real implementation:
    // window.location.href = exportUrl;
}

// Export single practice data
function exportPractice(practiceCode) {
    // Create export data for specific practice
    const exportUrl = `/api/export-practice/${practiceCode}/`;

    // For now, create a simple CSV export
    const rows = document.querySelectorAll(`#tableView tbody tr`);
    let csvContent = "Practice Name,Address,Postcode,Telephone,Health Board,Patient Count,GP Count,Patient/GP Ratio,Male Population,Female Population\n";

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 7) {
            const practiceName = cells[0].querySelector('strong').textContent.trim();
            const address = cells[0].querySelector('.text-muted').textContent.trim();
            const postcode = address.split('\n')[2] ? address.split('\n')[2].trim() : '';
            const telephone = cells[1].textContent.trim();
            const healthBoard = cells[2].textContent.trim();
            const patientCount = cells[3].querySelector('strong').textContent.trim();
            const gpCount = cells[4].querySelector('strong').textContent.trim();
            const ratio = cells[5].querySelector('strong').textContent.trim();
            const populationInfo = cells[5].querySelector('.population-info').textContent.trim();
            const popParts = populationInfo.split('\n');
            const malePop = popParts[0] ? popParts[0].replace('M', '').trim() : '0';
            const femalePop = popParts[1] ? popParts[1].replace('F', '').trim() : '0';

            csvContent += `"${practiceName}","${address}","${postcode}","${telephone}","${healthBoard}",${patientCount},${gpCount},${ratio},${malePop},${femalePop}\n`;
        }
    });

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `practice_data_${practiceCode}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Refresh data
function refreshData() {
    // Show loading state
    const refreshBtn = document.querySelector('[onclick="refreshData()"]');
    if (refreshBtn) {
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        refreshBtn.disabled = true;
    }

    // Reload the page
    setTimeout(() => {
        window.location.reload();
    }, 1000);
}

// Print current view
function printCurrentView() {
    window.print();
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + F: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.getElementById('search');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Ctrl/Cmd + R: Refresh data (prevent browser refresh)
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshData();
    }

    // Escape: Clear filters
    if (e.key === 'Escape') {
        clearFilters();
    }
});

// Clear all filters
function clearFilters() {
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        filterForm.reset();
        filterForm.submit();
    }
}

// Auto-refresh functionality (optional)
function setupAutoRefresh(interval = 300000) { // 5 minutes default
    setInterval(() => {
        // Only auto-refresh if user hasn't interacted recently
        const lastInteraction = sessionStorage.getItem('lastInteraction');
        const now = Date.now();

        if (!lastInteraction || (now - parseInt(lastInteraction)) > interval) {
            refreshData();
        }
    }, interval);

    // Track user interactions
    document.addEventListener('click', () => {
        sessionStorage.setItem('lastInteraction', Date.now().toString());
    });

    document.addEventListener('keypress', () => {
        sessionStorage.setItem('lastInteraction', Date.now().toString());
    });
}

// Initialize auto-refresh if needed
// setupAutoRefresh();

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function getRatioClass(ratio) {
    if (ratio > 2000) return 'text-danger';
    if (ratio > 1500) return 'text-warning';
    return 'text-success';
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Error handling
window.addEventListener('error', function (e) {
    console.error('Dashboard error:', e.error);
    // In production, you might want to send this to an error tracking service
});

// Performance monitoring
window.addEventListener('load', function () {
    const loadTime = performance.now();
    console.log(`Dashboard loaded in ${loadTime.toFixed(2)}ms`);
});