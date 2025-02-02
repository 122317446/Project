document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded! Filtering functions active."); // Debugging

    // ========== FILTER PRODUCTS ==========
    const filterButton = document.getElementById('apply-filters');
    if (filterButton) {
        filterButton.addEventListener('click', function (event) {
            event.preventDefault();

            console.log("Filter button clicked!");

            const usage = document.getElementById('filter-usage').value;
            const priceMin = document.getElementById('filter-price-min').value || 0;
            const priceMax = document.getElementById('filter-price-max').value || 1000000;
            const sortOrder = document.getElementById('sort-order').value;

            fetch(`/api/filter_products?usage=${usage}&price_min=${priceMin}&price_max=${priceMax}&sort=${sortOrder}`)
                .then(response => response.json())
                .then(data => {
                    const productGrid = document.getElementById('product-grid');
                    if (!productGrid) {
                        console.error("Product grid element not found!");
                        return;
                    }
                    productGrid.innerHTML = '';

                    data.forEach(product => {
                        const productElement = document.createElement('div');
                        productElement.className = 'col mb-5';
                        productElement.innerHTML = `
                            <div class="card h-100">
                                <img class="card-img-top" src="/static/images/${product.prodImage}" alt="..." />
                                <div class="card-body p-4">
                                    <div class="text-center">
                                        <h5 class="fw-bolder">${product.prodName}</h5>
                                        €${product.prodPrice}
                                    </div>
                                </div>
                                <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                    <div class="text-center">
                                        <a class="btn btn-outline-dark mt-auto" href="/Product/${product.prodID}">View</a>
                                    </div>
                                </div>
                            </div>
                        `;
                        productGrid.appendChild(productElement);
                    });
                })
                .catch(error => console.error('Error:', error));
        });
    }
});
