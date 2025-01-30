document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/stoic-quote")
        .then(response => response.json())
        .then(data => {
            console.log("Received API Data:", data); // Debugging

            // Access 'data' object inside the response
            if (data && data.data && data.data.quote && data.data.author) {
                document.getElementById("stoic-quote").innerText = `"${data.data.quote}"`;
                document.getElementById("stoic-author").innerText = `— ${data.data.author}`;
            } else {
                document.getElementById("stoic-quote").innerText = "Failed to load quote.";
                document.getElementById("stoic-author").innerText = "";
            }
        })
        .catch(error => {
            console.error("Error fetching quote:", error);
            document.getElementById("stoic-quote").innerText = "Error loading quote.";
        });
});
