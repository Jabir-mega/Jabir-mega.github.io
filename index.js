// const apiKey= "34569bbf11d04ab1aff832bb"; //variable to store api key 
// const apiUrl = "https://v6.exchangerate-api.com/v6/34569bbf11d04ab1aff832bb/latest/KES"; //base currency KES
// const apiUrl = "https://v6.exchangerate-api.com/v6/34569bbf11d04ab1aff832bb/latest/USD"; //base currency USD
let allRates = {};

// function to fetch data from the Exchange rate API
async function fetchExchangeRates() {
    try{
        // Show loading message and force browser to render it
        const loadingMessage = document.getElementById("loadingMessage");
        loadingMessage.style.display = "block";

        const baseCurrency = document.getElementById("baseCurrency").value; 
        // const apiUrl = "https://v6.exchangerate-api.com/v6/34569bbf11d04ab1aff832bb/latest/USD"; //base currency USD

        // const apiUrl= `https://v6.exchangerate-api.com/v6/34569bbf11d04ab1aff832bb/latest/${baseCurrency}`; //Base currency USD 
        console.log("URL with base currency: ", apiUrl);

        console.log("Fetching data...");
        const response = await fetch(apiUrl); // Fetches data from the API
        console.log("Response : ",response.status);

        const text = await response.text(); // Converts the response into javascript object
        console.log("raw response  : ",text);


        // const data = await response.json(); // Converts the response into javascript object
        const data = JSON.parse(text); // Converts the response into javascript object
        console.log("Parsed Data:", data);


        if (data.result === "success") {  // checks if it was success
            displayRates(data.conversion_rates); // if so passes it to this function
            displayAllRates(data.conversion_rates);
            allRates = data.conversion_rates;
        } else {
            console.error("Error fetching results", data); //this is else
        }
    } catch (error){ // this is the try cathc block
        console.error("Fetch error", error);
    } finally {
        loadingMessage.style.display = "none";
    }

}



// IN the above fucntion:
//  async allows us to use wait in the function which makes javascript wait for response before moving on

// function to display the specified rates 
function displayRates(rates) {
    const currencies = ['USD', 'CAD', 'AUD', 'QAR', 'EUR', 'GBP', 'KES']; //currencies interested in 
    const tableBody= document.getElementById('exchangeRates');
    tableBody.innerHTML = '';

    currencies.forEach(currency => {
        const ratePer$ = rates[currency] || "N/A";
        const ratePer100$ = rates[currency] ? (rates[currency] * 100).toFixed(4) : "N/A";
        const row = `<tr> 
                        <td>${currency}</td>
                        <td>${ratePer$}</td>
                        <td>${ratePer100$}</td>
                    </tr>`;
        
        tableBody.innerHTML += row;
    });
}
// function to display all the rates
function displayAllRates(rates){

    const tableBody = document.getElementById("foreing2");
    tableBody.innerHTML= '';

    Object.keys(rates).forEach(currency => {
        const ratePer$ = rates[currency] || "N/A";
        const ratePer100$ = rates[currency] ? (rates[currency] * 100).toFixed(4) : "N/A";
        const row = `<tr>
                        <td>${currency}</td>
                        <td>${ratePer$}</td>
                        <td>${ratePer100$}</td>
                    </tr>`;
        
        tableBody.innerHTML += row
    });
} 

// function that filters for the specified for user specific rates 
function filterRates() {
    const searchFilter = document.getElementById("currencySearch").value.toUpperCase();
    const filteredRates = {};
    
    Object.keys(allRates).forEach(currency => {
        if (currency.includes(searchFilter)){
            filteredRates[currency] = allRates[currency];
        }
    });

    // logic to check if the currency code exists and to display "NO Results found" if not 
    if (Object.keys(filteredRates).length === 0) {
        document.getElementById("noResultsMessage").style.display = "block";  // Show message
    } else {
        document.getElementById("noResultsMessage").style.display = "none";  // Hide message
        displayAllRates(filteredRates);
    }
}
function clearSearch() {
    document.getElementById("currencySearch").value = "";
    filterRates();  
}


// fetch data when page loads 
fetchExchangeRates();

// update data when drop down value changes 
document.getElementById("baseCurrency").addEventListener("change", fetchExchangeRates);
//update data when field is inputes
document.getElementById("currencySearch").addEventListener("input", filterRates);
// Auto-refresh every 5 minutes
setInterval(fetchExchangeRates, 300000);  // 300000 ms = 5 minutes


console.log(Object.keys);