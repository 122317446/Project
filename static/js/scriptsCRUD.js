document.addEventListener("DOMContentLoaded", function () {
    
    console.log("JavaScript Loaded!"); // Debugging

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

            fetch(`/updateProd/${prodID}`, {
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

            fetch(`/createProd`, {
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

            fetch(`/deleteProd/${prodID}`, {
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
