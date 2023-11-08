document.getElementById("scrape-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const url = document.getElementById("url").value;
  

    
    const status = document.getElementById("status");
    status.innerText = "Scraping in progress...";
});
