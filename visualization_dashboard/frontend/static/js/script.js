let allData = [];
let filteredData = [];
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('apply_filters')) {
        initDashboard();
    }
});

async function initDashboard() {
    await loadFilterOptions();

    document.getElementById('apply_filters').addEventListener('click', applyFilters);
    document.getElementById('reset_filters').addEventListener('click', resetFilters);
    document.getElementById('reload_data').addEventListener('click', reloadData);

    await applyFilters();
}

async function loadFilterOptions() {
    try {
        const response = await fetch('/api/filters/');
        if (!response.ok) {
            throw new Error('Failed to fetch filter options');
        }
        const data = await response.json();
        populateDropdown('end_year_filter', data.end_years);
        populateDropdown('topic_filter', data.topics);
        populateDropdown('sector_filter', data.sectors);
        populateDropdown('region_filter', data.regions);
        populateDropdown('pestle_filter', data.pestles);
        populateDropdown('source_filter', data.sources);
        populateDropdown('country_filter', data.countries);

    } catch (error) {
        console.error('Error loading filter options:', error);
        showError('Failed to load filter options. Please try again later.');
    }
}

function populateDropdown(elementId, options) {
    const select = document.getElementById(elementId);
    if (!select) return;

    while (select.options.length > 1) {
        select.remove(1);
    }
    options.forEach(option => {
        if (option) {
            const optElement = document.createElement('option');
            optElement.value = option;
            optElement.textContent = option;
            select.appendChild(optElement);
        }
    });
}

async function applyFilters() {
    try {
        document.querySelectorAll('.loading').forEach(el => {
            el.style.display = 'flex';
        });

        const params = new URLSearchParams();
        addFilterParam(params, 'end_year_filter', 'end_year');
        addFilterParam(params, 'topic_filter', 'topic');
        addFilterParam(params, 'sector_filter', 'sector');
        addFilterParam(params, 'region_filter', 'region');
        addFilterParam(params, 'pestle_filter', 'pestle');
        addFilterParam(params, 'source_filter', 'source');
        addFilterParam(params, 'country_filter', 'country');

        const statsResponse = await fetch(`/api/dashboard-stats/?${params}`);
        if (!statsResponse.ok) {
            throw new Error('Failed to fetch dashboard statistics');
        }

        const dataResponse = await fetch(`/api/filtered-data/?${params}`);
        if (!dataResponse.ok) {
            throw new Error('Failed to fetch filtered data');
        }

        const stats = await statsResponse.json();
        allData = await dataResponse.json();
        filteredData = [...allData];
        updateMetrics(stats);
        updateCharts(stats, allData);
        currentPage = 1;
        updateDataTable();

    } catch (error) {
        console.error('Error applying filters:', error);
        showError('Failed to update dashboard. Please try again later.');
    } finally {
        document.querySelectorAll('.loading').forEach(el => {
            el.style.display = 'none';
        });
    }
}

function addFilterParam(params, elementId, paramName) {
    const value = document.getElementById(elementId).value;
    if (value && value !== 'all') {
        params.append(paramName, value);
    }
}

function resetFilters() {
    document.querySelectorAll('.filter-section select').forEach(select => {
        select.value = 'all';
    });
    applyFilters();
}

async function reloadData() {
    try {
        if (!confirm('This will reload all data from the JSON file. Any changes in the database will be lost. Continue?')) {
            return;
        }
        const response = await fetch('/api/load-data/');
        if (!response.ok) {
            throw new Error('Failed to reload data');
        }
        const result = await response.json();
        alert(result.message);
        await loadFilterOptions();
        await applyFilters();
    } catch (error) {
        console.error('Error reloading data:', error);
        showError('Failed to reload data. Please try again later.');
    }
}

function updateMetrics(stats) {
    document.getElementById('avg_intensity').textContent = stats.intensity.avg || '0';
    document.getElementById('avg_likelihood').textContent = stats.likelihood.avg || '0';
    document.getElementById('avg_relevance').textContent = stats.relevance.avg || '0';
}

function updateCharts(stats, data) {
    createYearChart(stats.year_data);
    createRegionChart(stats.region_data);
    createTopicChart(stats.topic_data);
    createCountryChart(stats.country_data);
    createScatterChart(data);
    createSectorChart(stats.relevance_by_sector);
    createWorldMap(data);
}

function createYearChart(yearData) {
    const chart = document.getElementById('year_chart');
    chart.innerHTML = '';

    yearData = yearData.filter(item => item.end_year != null);
    if (yearData.length === 0) {
        chart.innerHTML = '<p>No data available for Year Chart.</p>';
        return;
    }
    const data = [{
        x: yearData.map(item => item.end_year),
        y: yearData.map(item => item.count),
        type: 'bar'
    }];
    const layout = {
        title: 'Intensity by Year',
        xaxis: { title: 'Year' },
        yaxis: { title: 'Count' }
    };
    Plotly.newPlot(chart, data, layout);
}

function createRegionChart(regionData) {
    const chart = document.getElementById('region_chart');
    chart.innerHTML = '';

    if (regionData.length === 0) {
        chart.innerHTML = '<p>No data available for Region Chart.</p>';
        return;
    }
    const data = [{
        labels: regionData.map(item => item.region),
        values: regionData.map(item => item.count),
        type: 'pie'
    }];
    const layout = {
        title: 'Data Distribution by Region'
    };
    Plotly.newPlot(chart, data, layout);
}

function createTopicChart(topicData) {
    const chart = document.getElementById('topic_chart');
    chart.innerHTML = '';

    if (topicData.length === 0) {
        chart.innerHTML = '<p>No data available for Topic Chart.</p>';
        return;
    }
    const data = [{
        x: topicData.map(item => item.topic),
        y: topicData.map(item => item.count),
        type: 'bar'
    }];
    const layout = {
        title: 'Topics Distribution',
        xaxis: { title: 'Topic' },
        yaxis: { title: 'Count' }
    };
    Plotly.newPlot(chart, data, layout);
}

function createCountryChart(countryData) {
    const chart = document.getElementById('country_chart');
    chart.innerHTML = '';

    if (countryData.length === 0) {
        chart.innerHTML = '<p>No data available for Country Chart.</p>';
        return;
    }
    const data = [{
        x: countryData.map(item => item.country),
        y: countryData.map(item => item.count),
        type: 'bar'
    }];
    const layout = {
        title: 'Country Distribution',
        xaxis: { title: 'Country' },
        yaxis: { title: 'Count' }
    };
    Plotly.newPlot(chart, data, layout);
}

function createScatterChart(data) {
    const chart = document.getElementById('scatter_chart');
    chart.innerHTML = '';

    if (data.length === 0) {
        chart.innerHTML = '<p>No data available for Scatter Chart.</p>';
        return;
    }
    const scatterData = [{
        x: data.map(item => item.intensity),
        y: data.map(item => item.likelihood),
        mode: 'markers',
        type: 'scatter',
        text: data.map(item => item.title)
    }];
    const layout = {
        title: 'Intensity vs Likelihood',
        xaxis: { title: 'Intensity' },
        yaxis: { title: 'Likelihood' }
    };
    Plotly.newPlot(chart, scatterData, layout);
}

function createSectorChart(sectorData) {
    const chart = document.getElementById('sector_chart');
    chart.innerHTML = '';

    if (sectorData.length === 0) {
        chart.innerHTML = '<p>No data available for Sector Chart.</p>';
        return;
    }
    const data = [{
        x: sectorData.map(item => item.sector),
        y: sectorData.map(item => item.relevance),
        type: 'bar'
    }];
    const layout = {
        title: 'Relevance by Sector',
        xaxis: { title: 'Sector' },
        yaxis: { title: 'Relevance' }
    };
    Plotly.newPlot(chart, data, layout);
}


function createWorldMap(data) {
    
}

function showError(message) {
    alert(message);
}

function updateDataTable() {
    const tableBody = document.getElementById('data_table_body');
    tableBody.innerHTML = '';
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    filteredData.slice(start, end).forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.intensity || 'NA'}</td>
            <td>${item.likelihood || 'NA'}</td>
            <td>${item.relevance || 'NA'}</td>
            <td>${item.end_year || 'NA'}</td>
            <td>${item.country || 'NA'}</td>
            <td>${item.topic || 'NA'}</td>
            <td>${item.region || 'NA'}</td>
        `;
        tableBody.appendChild(row);
    });
}




