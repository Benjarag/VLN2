document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('search-icon');

    document.getElementById("search-value").addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            searchBtn.click();
        }
    });

    searchBtn.addEventListener('click', async () => {
        const search = document.getElementById('search-value').value;
        const zip = document.getElementById('zip').value;
        const minPrice = document.getElementById('price-min').value;
        const maxPrice = document.getElementById('price-max').value;
        const type = document.getElementById('type').value;
        const orderByElement = document.getElementById('order-by');
        const orderBy = orderByElement ? orderByElement.value : "";

        let query = `?`;
        if (search) query += `search_filter=${encodeURIComponent(search)}&`;
        if (zip) query += `zip=${zip}&`;
        if (minPrice) query += `price_min=${minPrice}&`;
        if (maxPrice) query += `price_max=${maxPrice}&`;
        if (type) query += `type=${type}&`;
        if (orderBy) query += `order_by=${orderBy}`;

        const response = await fetch(`/properties/${query}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        const properties = data.data;

        const container = document.getElementById('properties-placeholder');
        container.innerHTML = properties.map(renderPropertyCard).join('');
    });

    function renderPropertyCard(property) {
        const isSold = property.status.toLowerCase() === 'sold';
        return `
            <div class="property-card" data-id="{{ property.id }}">
                <div class="property-image-wrapper">
                    <img src="{% static property.image_url %}" class="property-image" alt="Property image">
                    <div class="property-status {{ property.status|lower }}">{{ property.status }}</div>
                    <div class="favorite-icon">&#9825;</div>
                </div>

                <div class="property-info">
                    <div class="property-address">
                        <span class="location-icon">&#x1F4CD;</span> {{ property.title }}
                    </div>
                    <div class="property-details">
                        <span class="detail-box">🏠 {{ property.size }} sqm</span>
                        <span class="detail-box">🛏️ {{ property.rooms }} rooms</span>
                    </div>
                    <div class="property-price">{{ property.get_formatted_price }} kr.</div>
                </div>
            </div>
        `;
    }

});
