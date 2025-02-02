document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const suggestionsList = document.getElementById('suggestions-list');

    // Function to fetch and display suggestions
    const fetchSuggestions = (query) => {
        fetch(`/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsList.innerHTML = ''; // Clear previous suggestions
                data.forEach(product => {
                    const li = document.createElement('li');
                    li.textContent = product.prodName;
                    li.style.cursor = 'pointer';

                    li.addEventListener('click', () => {
                        window.location.href = `/Product/${product.prodID}`;
                    });

                    suggestionsList.appendChild(li);
                });
            });
    };

    // Event listener for input changes
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();
        if (query) {
            fetchSuggestions(query);
        } else {
            suggestionsList.innerHTML = ''; // Clear suggestions when input is empty
        }
    });
});

document.addEventListener('click', (event) => {
    const searchContainer = document.querySelector('.search-container');
    // If the clicked element is not inside the search container...
    if (!searchContainer.contains(event.target)) {
        const suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = ''; // Clear the suggestions list
    }
});
