// Ensure the DOM is fully loaded before executing any scripts
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('price-chart').getContext('2d');

    // Function to render the chart
    function renderChart(priceHistory) {
        // Prepare labels and data for the chart
        const labels = priceHistory.map(entry => entry.id);
        const data = priceHistory.map(entry => parseFloat(entry.price.replace("₹", "").replace(",", "").trim()));

        // Create the chart
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price Over Time',
                    data: data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    }

    // Fetch price history data from the server
    async function fetchPriceHistory(productId) {
        try {
            const response = await fetch(`/api/price-history/${productId}`); // Adjust the URL to your API endpoint
            if (!response.ok) throw new Error('Network response was not ok');
            const priceHistory = await response.json();
            renderChart(priceHistory);
        } catch (error) {
            console.error('Error fetching price history:', error);
        }
    }

    // Call the function to fetch and display the price history for a specific product
    const productId = '{{ product.id }}'; // Get the product ID from the Flask template
    if (productId) {
        fetchPriceHistory(productId);
    }
});
