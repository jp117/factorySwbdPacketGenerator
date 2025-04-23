// Form Module - Handles form validation and submission
const FormModule = {
    requiredFields: [
        'sales_order',
        'customer_name',
        'job_address',
        'switchboard_name',
        'num_sections'
    ],

    validate() {
        for (const field of this.requiredFields) {
            const input = document.getElementById(field);
            if (!input?.value.trim()) {
                this.showError(`Please fill in the ${field.replace('_', ' ')}`);
                input?.focus();
                return false;
            }
        }

        // Validate common settings
        if (!this.validateCommonSettings()) {
            return false;
        }

        if (!this.validateSectionTypes()) {
            return false;
        }

        return true;
    },

    validateCommonSettings() {
        // Check if height is 90"
        const selectedHeight = document.querySelector('input[name="common_height"]:checked')?.value;
        if (selectedHeight !== '90') {
            this.showError('Only 90" tall boards are programmed right now.');
            return false;
        }

        // Check if depth is 30" or 36"
        const selectedDepth = document.querySelector('input[name="common_depth"]:checked')?.value;
        if (selectedDepth !== '30' && selectedDepth !== '36') {
            this.showError('Only 30" or 36" depth is programmed right now.');
            return false;
        }

        return true;
    },

    validateSectionTypes() {
        const sections = document.querySelectorAll('.section-card');
        let hasSectionType = false;
        sections.forEach(section => {
            const typeSelect = section.querySelector('select[name^="section_type"]');
            if (typeSelect?.value) {
                hasSectionType = true;
            }
        });

        if (!hasSectionType) {
            this.showError('Please select a section type for at least one section');
            return false;
        }

        return true;
    },

    showError(message) {
        alert(message); // TODO: Replace with a better UI feedback mechanism
    }
};

// Image Selection Module - Handles image selection based on section configuration
const ImageSelectionModule = {
    // Get images for a specific section
    getImagesForSection(sectionNumber, totalSections, sectionType, width, amperage, depth) {
        const images = [];
        
        if (sectionType === 'Spectra') {
            // Check if this is a first or last section
            const isFirstOrLast = sectionNumber === 1 || sectionNumber === totalSections;
            
            // Add ABC and Neutral images for first/last sections
            if (isFirstOrLast) {
                if (width === '44') {
                    images.push({
                        name: '38x4spectraHorizontalABC.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                    images.push({
                        name: '38x4spectraHorizontalNuetral.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                } else if (width === '40') {
                    images.push({
                        name: '38x4spectraHorizontalABC.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                    images.push({
                        name: '38x4spectraHorizontalNuetral.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                }
            } else {
                // Middle section images
                if (width === '44') {
                    images.push({
                        name: '43x4spectraHorizontalABC.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                    images.push({
                        name: '43x4spectraHorizontalNuetral.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                } else if (width === '40') {
                    images.push({
                        name: '43x4spectraHorizontalABC.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                    images.push({
                        name: '43x4spectraHorizontalNuetral.png',
                        quantity: this.getQuantityForAmperage(amperage)
                    });
                }
            }
            
            // Add B-link images (2 per section)
            images.push({
                name: '95x4spectraBLink.png',
                quantity: 2
            });
            
            // Add AC-link images (2 of each per section)
            images.push({
                name: '115x4spectraACLink1.png',
                quantity: 2
            });
            images.push({
                name: '115x4spectraACLink2.png',
                quantity: 2
            });
            
            // Add connection bar stack images based on depth and amperage
            if (depth === '30') {
                images.push({
                    name: this.getConnectionBarStackImage(amperage, '30'),
                    quantity: 6
                });
            } else if (depth === '36') {
                images.push({
                    name: this.getConnectionBarStackImage(amperage, '36'),
                    quantity: 6
                });
            }
            
            // Add AC phase vertical link (4 per section)
            images.push({
                name: '1225x4spectraACPhaseVerticalLink4in.png',
                quantity: 4
            });
            
            // Add inner steel images for 44" width
            if (width === '44') {
                images.push({
                    name: '44375SpectraInnerSteel44Wide.png',
                    quantity: 2
                });
                images.push({
                    name: '44375SpectraInnerSteel44WideSideView.png',
                    quantity: 1
                });
            }
        }
        
        return images;
    },
    
    // Get quantity based on amperage
    getQuantityForAmperage(amperage) {
        switch (amperage) {
            case '4000':
                return 4;
            case '3000':
            case '2500':
                return 3;
            case '2000':
            case '1200':
                return 2;
            case '1000':
                return 1;
            default:
                return 1;
        }
    },
    
    // Get connection bar stack image based on amperage and depth
    getConnectionBarStackImage(amperage, depth) {
        if (depth === '30') {
            switch (amperage) {
                case '4000':
                    return '675x4SpectraHorizontalConnection4BarStack30deep.png';
                case '3000':
                case '2500':
                    return '725x4SpectraHorizontalConnection3BarStack30deep.png';
                case '2000':
                case '1200':
                    return '775x4SpectraHorizontalConnection2BarStack30deep.png';
                case '1000':
                    return '825x4SpectraHorizontalConnection1BarStack30Deep';
                default:
                    return '825x4SpectraHorizontalConnection1BarStack30Deep';
            }
        } else if (depth === '36') {
            switch (amperage) {
                case '4000':
                    return '1275x4SpectraHorizontalConnection4BarStack36deep.png';
                case '3000':
                case '2500':
                    return '1325x4SpectraHorizontalConnection3BarStack36deep';
                case '2000':
                case '1200':
                    return '1375x4SpectraHorizontalConnection2BarStack36deep';
                case '1000':
                    return '1425x4SpectraHorizontalConnection1BarStack36deep';
                default:
                    return '1425x4SpectraHorizontalConnection1BarStack36deep';
            }
        }
    }
};

// Common Settings Module - Handles common settings toggles and state
const CommonSettingsModule = {
    settings: {
        depth: {
            name: 'common_depth',
            toggle: 'toggleCommonDepth',
            selector: 'input[name^="depth_"]'
        },
        height: {
            name: 'common_height',
            toggle: 'toggleCommonHeight',
            selector: 'input[name^="height_"]'
        },
        amperage: {
            name: 'common_amperage',
            toggle: 'toggleCommonAmperage',
            selector: 'select[name^="amperage_"]'
        },
        bus: {
            name: 'common_bus',
            toggle: 'toggleCommonBus',
            selector: 'select[name^="bus_"]'
        }
    },

    toggleSetting(setting) {
        const selectedValue = document.querySelector(`input[name="${setting.name}"]:checked`)?.value;
        console.log(`Toggle ${setting.name} called:`, selectedValue);
        
        const sectionCards = document.querySelectorAll('.section-card');
        sectionCards.forEach(card => {
            const input = card.querySelector(setting.selector);
            if (input) {
                const container = input.closest('div');
                container.style.display = selectedValue === 'no' ? 'block' : 'none';
                if (input.tagName === 'INPUT') {
                    input.disabled = selectedValue !== 'no';
                }
            }
        });
    },

    toggleCommonDepth() {
        this.toggleSetting(this.settings.depth);
    },

    toggleCommonHeight() {
        this.toggleSetting(this.settings.height);
    },

    toggleCommonAmperage() {
        this.toggleSetting(this.settings.amperage);
    },

    toggleCommonBus() {
        this.toggleSetting(this.settings.bus);
    },

    applyAllSettings() {
        this.toggleCommonDepth();
        this.toggleCommonHeight();
        this.toggleCommonAmperage();
        this.toggleCommonBus();
    },

    initializeEventListeners() {
        Object.values(this.settings).forEach(setting => {
            document.querySelectorAll(`input[name="${setting.name}"]`).forEach(radio => {
                radio.addEventListener('change', () => this[setting.toggle]());
            });
        });
    }
};

// Section Module - Handles section card creation and management
const SectionModule = {
    createCard(sectionNumber) {
        const card = document.createElement('div');
        card.className = 'section-card bg-white rounded-lg shadow-sm p-6';
        card.id = `section-${sectionNumber}`;
        
        card.innerHTML = this.getCardTemplate(sectionNumber);
        
        // Add event listener for section type change
        const typeSelect = card.querySelector(`select[name="section_type_${sectionNumber}"]`);
        if (typeSelect) {
            typeSelect.addEventListener('change', (e) => this.handleSectionTypeChange(e, sectionNumber));
        }
        
        return card;
    },

    handleSectionTypeChange(event, sectionNumber) {
        const sectionType = event.target.value;
        const widthSelect = document.querySelector(`select[name="width_${sectionNumber}"]`);
        
        if (widthSelect) {
            // Clear existing options
            widthSelect.innerHTML = '';
            
            if (sectionType === 'MLO') {
                // Add only 36" option for MLO
                const option = document.createElement('option');
                option.value = '36';
                option.textContent = '36"';
                widthSelect.appendChild(option);
                widthSelect.disabled = true;
            } else if (sectionType === 'Spectra') {
                // Add 40" and 44" options for Spectra
                const option40 = document.createElement('option');
                option40.value = '40';
                option40.textContent = '40"';
                widthSelect.appendChild(option40);
                
                const option44 = document.createElement('option');
                option44.value = '44';
                option44.textContent = '44"';
                widthSelect.appendChild(option44);
                
                // Default to 44"
                widthSelect.value = '44';
                widthSelect.disabled = false;
            } else {
                widthSelect.disabled = true;
            }
        }
    },

    getCardTemplate(sectionNumber) {
        return `
            <div class="flex items-center gap-4 mb-4">
                <h3 class="text-lg font-medium text-gray-900">Section ${sectionNumber}</h3>
                <select name="section_type_${sectionNumber}" class="px-3 py-1.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" required>
                    <option value="">Select type</option>
                    <option value="MLO">MLO</option>
                    <option value="Spectra">Spectra</option>
                </select>
            </div>
            <div class="grid grid-cols-1 gap-4 mb-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Width (inches)</label>
                    <select name="width_${sectionNumber}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" disabled>
                        <option value="">Select section type first</option>
                    </select>
                </div>
                <div style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Depth (inches)</label>
                    <input type="number" name="depth_${sectionNumber}" step="0.01" min="0"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Height (inches)</label>
                    <input type="number" name="height_${sectionNumber}" step="0.01" min="0"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Amperage</label>
                    <select name="amperage_${sectionNumber}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option value="1000">1000A</option>
                        <option value="1200">1200A</option>
                        <option value="2000">2000A</option>
                        <option value="2500">2500A</option>
                        <option value="3000">3000A</option>
                        <option value="4000">4000A</option>
                    </select>
                </div>
                <div style="display: none;">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Bus Size (inches)</label>
                    <select name="bus_${sectionNumber}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option value="4">4"</option>
                    </select>
                </div>
            </div>
        `;
    },

    updateCards() {
        const numSections = parseInt(document.getElementById('num_sections')?.value) || 0;
        const container = document.getElementById('section-cards');
        if (!container) return;

        container.innerHTML = '';
        for (let i = 1; i <= numSections; i++) {
            container.appendChild(this.createCard(i));
        }

        // Re-apply common settings
        CommonSettingsModule.applyAllSettings();
    }
};

// Event Handlers Module - Centralizes all event handling
const EventHandlersModule = {
    initialize() {
        // Form submission
        const form = document.getElementById('packetForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!FormModule.validate()) {
                    e.preventDefault();
                }
            });
        }

        // Number of sections change
        const numSectionsInput = document.getElementById('num_sections');
        if (numSectionsInput) {
            numSectionsInput.addEventListener('change', () => SectionModule.updateCards());
        }

        // Initialize common settings
        CommonSettingsModule.initializeEventListeners();
        CommonSettingsModule.applyAllSettings();
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    EventHandlersModule.initialize();
}); 