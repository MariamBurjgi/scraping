document.getElementById("scrape-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const url = document.getElementById("url").value;
    const status = document.getElementById("status");
    const resultsTable = document.getElementById("results");

    status.innerText = "Scraping in progress...";

    
    fetch('/scrape', {
        method: 'POST',
        body: JSON.stringify({ url }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((data) => {
        
       
    })
    .catch((error) => {
        
        status.innerText = "Error: " + error.message;
    });
});

