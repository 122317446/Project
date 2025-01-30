document.addEventListener("DOMContentLoaded", function () {

    console.log("User Management JS Loaded!"); // Debugging

    // ========== CREATE USER ==========
    const createUserForm = document.getElementById("createUserForm");
    if (createUserForm) {
        createUserForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            console.log("Create User Form Submitted!");

            const formData = new FormData(this);

            fetch(`/create_user`, {
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
                alert("Error: Failed to create user.");
            });
        });
    }

    // ========== EDIT USER ==========
    const editUserButtons = document.querySelectorAll(".edit-user-btn");

    editUserButtons.forEach(button => {
        button.addEventListener("click", function () {
            console.log("Edit button clicked!");

            // Get user data from button attributes
            document.getElementById("edit-user-id").value = this.getAttribute("data-user-id");
            document.getElementById("edit-user-firstname").value = this.getAttribute("data-user-firstname");
            document.getElementById("edit-user-lastname").value = this.getAttribute("data-user-lastname");
            document.getElementById("edit-user-email").value = this.getAttribute("data-user-email");
            document.getElementById("edit-user-address").value = this.getAttribute("data-user-address");
            document.getElementById("edit-user-phone").value = this.getAttribute("data-user-phone");
        });
    });

    // ========== UPDATE USER ==========
    const updateUserForm = document.getElementById("editUserForm");
    if (updateUserForm) {
        updateUserForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            console.log("Update User Form Submitted!");

            const formData = new FormData(this);
            const userID = formData.get("userID");

            fetch(`/update_user/${userID}`, {
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
                alert("Error: Failed to update user.");
            });
        });
    }

    // ========== DELETE USER ==========
    const deleteUserButtons = document.querySelectorAll(".delete-user-btn");

    deleteUserButtons.forEach(button => {
        button.addEventListener("click", function () {
            const userID = this.getAttribute("data-user-id");

            if (!confirm("Are you sure you want to delete this user?")) {
                return; // User canceled deletion
            }

            fetch(`/delete_user/${userID}`, {
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
                alert("Error: Failed to delete user.");
            });
        });
    });

});
