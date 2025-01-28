document.addEventListener("DOMContentLoaded", function () {
    
    console.log("JavaScript Loaded!"); // Debugging

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

    // ========== VIEW PRODUCT ATTRIBUTES ==========
    const editButtons = document.querySelectorAll(".edit-btn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            console.log("Edit button clicked!");

            // Get product data from button attributes
            const prodID = this.getAttribute("data-prod-id");
            const prodName = this.getAttribute("data-prod-name");
            const prodDesc = this.getAttribute("data-prod-desc");
            const prodPrice = this.getAttribute("data-prod-price");
            const prodStock = this.getAttribute("data-prod-stock");
            const prodUsage = this.getAttribute("data-prod-usage");
            const prodAttributes = this.getAttribute("data-prod-attributes");

            console.log("Product Data for Edit:", { prodID, prodName, prodDesc, prodPrice, prodStock, prodUsage, prodAttributes });

            // Populate modal fields
            document.getElementById("edit-prod-id").value = prodID;
            document.getElementById("edit-prod-name").value = prodName;
            document.getElementById("edit-prod-desc").value = prodDesc;
            document.getElementById("edit-prod-price").value = prodPrice;
            document.getElementById("edit-prod-stock").value = prodStock;
            document.getElementById("edit-prod-usage").value = prodUsage;
            document.getElementById("edit-prod-attributes").value = prodAttributes;
        });
    });

    // ========== UPDATE PRODUCT ==========
    const updateProductForm = document.getElementById("editProductForm");
    if (updateProductForm) {
        updateProductForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            console.log("Update Product Form Submitted!");

            const formData = new FormData(this);
            const prodID = formData.get("prodID");

            fetch(`/update_product/${prodID}`, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Update Response:", data);
                alert(data.message);
                location.reload();  // Refresh page after update
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error: Failed to update product.");
            });
        });
    }

    // ========== CREATE PRODUCT ==========
    const createProductForm = document.getElementById("createProductForm");
    if (createProductForm) {
        createProductForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            console.log("Create Product Form Submitted!");

            const formData = new FormData(this);

            fetch(`/create_product`, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Create Response:", data);
                alert(data.message);
                location.reload();  // Refresh page after creation
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error: Failed to create product.");
            });
        });
    }

    // ========== DELETE PRODUCT ==========
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const prodID = this.getAttribute("data-prod-id");

            if (!confirm("Are you sure you want to delete this product?")) {
                return; // User canceled deletion
            }

            fetch(`/delete_product/${prodID}`, {
                method: "DELETE"
            })
            .then(response => response.json())
            .then(data => {
                console.log("Delete Response:", data);
                alert(data.message);
                location.reload();  // Refresh page after deletion
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Error: Failed to delete product.");
            });
        });
    });

});
