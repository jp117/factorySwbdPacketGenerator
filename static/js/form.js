// Form validation
function validateForm() {
    const requiredFields = [
        'sales_order',
        'customer_name',
        'job_address',
        'switchboard_name',
        'num_sections'
    ];

    for (const field of requiredFields) {
        const input = document.getElementById(field);
        if (!input.value.trim()) {
            alert(`Please fill in the ${field.replace('_', ' ')}`);
            input.focus();
            return false;
        }
    }

    // Check if at least one section type is selected
    const sections = document.querySelectorAll('.section-card');
    let hasSectionType = false;
    sections.forEach(section => {
        const typeSelect = section.querySelector('select[name^="section_type"]');
        if (typeSelect && typeSelect.value) {
            hasSectionType = true;
        }
    });

    if (!hasSectionType) {
        alert('Please select a section type for at least one section');
        return false;
    }

    return true;
}

// Common settings handlers
function toggleCommonDepth() {
    const selectedDepth = document.querySelector('input[name="common_depth"]:checked')?.value;
    const depthInputs = document.querySelectorAll('input[name^="depth_"]');
    
    depthInputs.forEach(input => {
        const sectionCard = input.closest('.section-card');
        if (sectionCard) {
            input.disabled = selectedDepth !== null;
            input.value = selectedDepth || '';
        }
    });
}

function toggleCommonHeight() {
    const selectedHeight = document.querySelector('input[name="common_height"]:checked')?.value;
    const heightInputs = document.querySelectorAll('input[name^="height_"]');
    
    heightInputs.forEach(input => {
        const sectionCard = input.closest('.section-card');
        if (sectionCard) {
            input.disabled = selectedHeight !== null;
            input.value = selectedHeight || '';
        }
    });
}

// Section card management
function updateSectionCards() {
    const numSections = parseInt(document.getElementById('num_sections').value) || 0;
    const container = document.getElementById('section-cards');
    container.innerHTML = '';

    for (let i = 1; i <= numSections; i++) {
        const card = createSectionCard(i);
        container.appendChild(card);
    }

    // Re-apply common settings
    toggleCommonDepth();
    toggleCommonHeight();
}

// Function to create a section card
function createSectionCard(sectionNumber) {
    const card = document.createElement('div');
    card.className = 'section-card bg-white rounded-lg shadow-sm p-6';
    
    const header = document.createElement('div');
    header.className = 'flex items-center gap-4 mb-4';
    
    const title = document.createElement('h3');
    title.className = 'text-lg font-medium text-gray-900';
    title.textContent = `Section ${sectionNumber}`;
    
    const typeSelect = document.createElement('select');
    typeSelect.name = `section_type_${sectionNumber}`;
    typeSelect.className = 'px-3 py-1.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm';
    typeSelect.required = true;
    
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Select type';
    typeSelect.appendChild(defaultOption);
    
    const mloOption = document.createElement('option');
    mloOption.value = 'MLO';
    mloOption.textContent = 'MLO';
    typeSelect.appendChild(mloOption);
    
    const spectraOption = document.createElement('option');
    spectraOption.value = 'Spectra';
    spectraOption.textContent = 'Spectra';
    typeSelect.appendChild(spectraOption);
    
    header.appendChild(title);
    header.appendChild(typeSelect);
    
    const dimensions = document.createElement('div');
    dimensions.className = 'grid grid-cols-1 gap-4 mb-4';
    
    const widthDiv = document.createElement('div');
    widthDiv.innerHTML = `
        <label class="block text-sm font-medium text-gray-700 mb-1">Width (inches)</label>
        <input type="number" name="width_${sectionNumber}" step="0.01" min="0"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
    `;
    
    dimensions.appendChild(widthDiv);
    
    card.appendChild(header);
    card.appendChild(dimensions);
    
    return card;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const numSections = document.getElementById('num_sections').value;
    if (numSections) {
        updateSectionCards();
    }
}); 