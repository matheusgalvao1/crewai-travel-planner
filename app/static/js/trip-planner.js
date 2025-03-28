document.getElementById('tripForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show loading spinner and results card
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('resultsCard').style.display = 'block';
    document.getElementById('resultsContent').innerHTML = '';

    const formData = new FormData(this);

    try {
        const response = await fetch('/plan', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        console.log('Response data:', data); // Debug log
        
        if (response.ok && data) {
            // Display the itinerary
            let html = '<div class="itinerary">';
            if (data.daily_plans && Array.isArray(data.daily_plans)) {
                data.daily_plans.forEach((day, index) => {
                    html += `
                        <div class="day-plan mb-4">
                            <h6>Day ${index + 1}</h6>
                            <ul class="list-group">
                                ${day.attractions.map(attraction => `
                                    <li class="list-group-item">
                                        <strong>${attraction.name}</strong><br>
                                        ${attraction.description}
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    `;
                });
                
                // Add overall tips if available
                if (data.overall_tips) {
                    html += `
                        <div class="overall-tips mt-4">
                            <h6>Overall Tips</h6>
                            <div class="alert alert-info">
                                ${data.overall_tips}
                            </div>
                        </div>
                    `;
                }
            } else {
                html += '<div class="alert alert-warning">No itinerary data available</div>';
            }
            html += '</div>';
            document.getElementById('resultsContent').innerHTML = html;
        } else {
            // Display error message
            document.getElementById('resultsContent').innerHTML = `
                <div class="alert alert-danger">
                    ${data.error || 'An error occurred while planning your trip.'}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error:', error); // Debug log
        document.getElementById('resultsContent').innerHTML = `
            <div class="alert alert-danger">
                An error occurred while planning your trip. Please try again.
            </div>
        `;
    } finally {
        // Hide loading spinner
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}); 