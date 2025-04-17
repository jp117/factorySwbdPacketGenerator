document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('packetForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading overlay
        loadingOverlay.classList.remove('hidden');
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        try {
            // Send request to backend
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Download the generated PDF
                window.location.href = result.file_url;
                alert('PDF packet generated successfully!');
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            alert('Error generating PDF packet: ' + error.message);
        } finally {
            // Hide loading overlay
            loadingOverlay.classList.add('hidden');
        }
    });
});

function selectAll() {
    document.querySelectorAll('input[name="selected_items"]').forEach(checkbox => {
        checkbox.checked = true;
    });
}

function deselectAll() {
    document.querySelectorAll('input[name="selected_items"]').forEach(checkbox => {
        checkbox.checked = false;
    });
} 