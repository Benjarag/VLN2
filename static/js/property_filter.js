document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-icon');
    
    // 1. Add a reset button to the HTML
    const filterContainer = document.querySelector('.filter-container');
    const resetButton = document.createElement('button');
    resetButton.id = 'reset-filter';
    resetButton.textContent = 'Reset Filter';
    
    // Create a new filter group for the reset button
    const resetFilterGroup = document.createElement('div');
    resetFilterGroup.className = 'filter-group';
    resetFilterGroup.appendChild(resetButton);
    
    // Add reset button after the search button
    const searchButtonGroup = document.querySelector('.filter-group:last-child');
    filterContainer.insertBefore(resetFilterGroup, searchButtonGroup.nextSibling);
    
    // 2. Load saved filters from localStorage
    loadSavedFilters();
    
    // Apply filters from URL on initial page load (for back button navigation)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.toString()) {
        applyFiltersFromParams(urlParams);
    } else if (window.location.pathname === '/properties/') {
        // If we're at the root properties URL with no params,
        // check if we arrived by back button or direct navigation
        const shouldShowAll = sessionStorage.getItem('show_all_properties');
        if (shouldShowAll === 'true') {
            // Reset filters
            clearFilters();
            // Reset the flag
            sessionStorage.removeItem('show_all_properties');
        }
    }

    // Add event listener for browser back/forward navigation
    window.addEventListener('popstate', function(event) {
        console.log('Navigation state changed:', window.location.href);
        
        // Get the new URL params after back/forward navigation
        const newUrlParams = new URLSearchParams(window.location.search);
        
        // If we navigated to the root properties URL with no params
        if (window.location.pathname === '/properties/' && !newUrlParams.toString()) {
            console.log('At root with no params, clearing filters');
            // Set flag to show all properties
            sessionStorage.setItem('show_all_properties', 'true');
            // Clear and reset filters
            clearFilters();
            // Fetch all properties
            fetchProperties('');
        } else {
            // Apply the URL parameters as filters
            applyFiltersFromParams(newUrlParams);
        }
    });

    document.getElementById("search-value").addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            searchBtn.click();
        }
    });

    // Reset filter button event listener
    resetButton.addEventListener('click', () => {
        clearFilters();
        
        // Reset URL
        history.pushState({}, '', '/properties/');
        
        // Fetch all properties
        fetchProperties('');
    });
    
    // Function to clear all filters
    function clearFilters() {
        // Clear all inputs
        document.getElementById('search-value').value = '';
        document.getElementById('zip').value = '';
        document.getElementById('price-min').value = '';
        document.getElementById('price-max').value = '';
        document.getElementById('type').value = '';
        
        const orderByElement = document.getElementById('order-by');
        if (orderByElement) {
            orderByElement.value = '';
        }
        
        // Clear localStorage and sessionStorage
        localStorage.removeItem('property_filters');
        sessionStorage.removeItem('show_all_properties');
    }

    searchBtn.addEventListener('click', async () => {
        const search = document.getElementById('search-value').value;
        const zip = document.getElementById('zip').value;
        const minPrice = document.getElementById('price-min').value;
        const maxPrice = document.getElementById('price-max').value;
        const type = document.getElementById('type').value;
        const orderByElement = document.getElementById('order-by');
        const orderBy = orderByElement ? orderByElement.value : "";

        // Build query string
        let query = `?`;
        if (search) query += `search_filter=${encodeURIComponent(search)}&`;
        if (zip) query += `zip=${zip}&`;
        if (minPrice) query += `price_min=${minPrice}&`;
        if (maxPrice) query += `price_max=${maxPrice}&`;
        if (type) query += `type=${type}&`;
        if (orderBy) query += `order_by=${orderBy}`;
        
        // Remove trailing & if exists
        if (query.endsWith('&')) {
            query = query.slice(0, -1);
        }
        
        // If no filters, just show "?" in the URL
        if (query === '?') {
            query = '';
        }
        
        // Save filter settings to localStorage
        saveFilters({
            search_filter: search,
            zip: zip,
            price_min: minPrice,
            price_max: maxPrice,
            type: type,
            order_by: orderBy
        });
        
        // Update URL with filters (for back button functionality)
        history.pushState({filters: true}, '', `/properties/${query}`);
        
        // Fetch filtered properties
        fetchProperties(query);
    });
    
    // Function to save filter settings to localStorage
    function saveFilters(filters) {
        localStorage.setItem('property_filters', JSON.stringify(filters));
    }
    
    // Function to load saved filters from localStorage
    function loadSavedFilters() {
        const savedFilters = localStorage.getItem('property_filters');
        if (savedFilters) {
            const filters = JSON.parse(savedFilters);
            
            // Set form values
            if (filters.search_filter) document.getElementById('search-value').value = filters.search_filter;
            if (filters.zip) document.getElementById('zip').value = filters.zip;
            if (filters.price_min) document.getElementById('price-min').value = filters.price_min;
            if (filters.price_max) document.getElementById('price-max').value = filters.price_max;
            if (filters.type) document.getElementById('type').value = filters.type;
            
            const orderByElement = document.getElementById('order-by');
            if (orderByElement && filters.order_by) {
                orderByElement.value = filters.order_by;
            }
        }
    }
    
    // Function to apply filters from URL parameters
    function applyFiltersFromParams(params) {
        if (params.has('search_filter')) document.getElementById('search-value').value = params.get('search_filter');
        if (params.has('zip')) document.getElementById('zip').value = params.get('zip');
        if (params.has('price_min')) document.getElementById('price-min').value = params.get('price_min');
        if (params.has('price_max')) document.getElementById('price-max').value = params.get('price_max');
        if (params.has('type')) document.getElementById('type').value = params.get('type');
        
        const orderByElement = document.getElementById('order-by');
        if (orderByElement && params.has('order_by')) {
            orderByElement.value = params.get('order_by');
        }
        
        // If no params, clear filters
        if (params.toString() === '') {
            clearFilters();
        } else {
            // Save these filters to localStorage as well
            const filterObj = {};
            for (const [key, value] of params.entries()) {
                filterObj[key] = value;
            }
            saveFilters(filterObj);
        }
        
        // Only fetch if we're on the main listing page (not coming from a property detail)
        if (document.getElementById('properties-placeholder')) {
            fetchProperties(params.toString() ? '?' + params.toString() : '');
        }
    }
    
    // Refactored fetch function to avoid code duplication
    async function fetchProperties(query) {
        const response = await fetch(`/properties/${query}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        const properties = data.data;
        
        // Debug line to see what's coming back
        console.log('Properties from API:', properties);

        const container = document.getElementById('properties-placeholder');
        container.innerHTML = properties.map(renderPropertyCard).join('');
        
        // Reattach event listeners after updating DOM
        attachPropertyCardEventListeners();
    }

    function renderPropertyCard(property) {
        const isSold = property.status.toLowerCase() === 'sold';
        
        // Handle image URL correctly
        const imageUrl = property.image_url || '';
        
        return `
            <div class="property-card" data-id="${property.id}">
                <div class="property-image-wrapper">
                    <img src="/static/${imageUrl}" class="property-image" alt="Property image">
                    <div class="property-status ${property.status.toLowerCase()}">${property.status}</div>
                    <div class="favorite-icon">&#9825;</div>
                </div>

                <div class="property-info">
                    <div class="property-address">
                        <span class="location-icon">&#x1F4CD;</span> ${property.title}
                    </div>
                    <div class="property-details">
                        <span class="detail-box">🏠 ${property.size} sqm</span>
                        <span class="detail-box">🛏️ ${property.rooms} rooms</span>
                    </div>
                    <div class="property-price">${property.price} kr.</div>
                </div>
            </div>
        `;
    }
    
    // Function to attach event listeners to property cards
    function attachPropertyCardEventListeners() {
        // Handle favorite icon clicks
        document.querySelectorAll('.favorite-icon').forEach(icon => {
            icon.addEventListener('click', function(e) {
                // Toggle the active class
                this.classList.toggle('active');
                
                // Toggle between empty and filled heart entities
                if (this.classList.contains('active')) {
                    this.innerHTML = '♥'; // Filled heart
                } else {
                    this.innerHTML = '&#9825;'; // Outline heart
                }
                
                // Prevent the click from bubbling up to the parent
                e.stopPropagation();
                e.preventDefault();
                
                // Here you would normally add AJAX to save the favorite status
                console.log('Favorite toggled');
            });
        });
        
        // Make property cards clickable
        document.querySelectorAll('.property-card').forEach(card => {
            card.addEventListener('click', function(e) {
                // Don't redirect if the favorite icon was clicked
                if (e.target.closest('.favorite-icon')) {
                    return;
                }
                
                // Get the property ID from the data attribute
                const propertyId = this.getAttribute('data-id');
                if (propertyId) {
                    window.location.href = `/properties/${propertyId}/`;
                }
            });
        });
    }
    
    // Attach event listeners on initial page load
    attachPropertyCardEventListeners();
});