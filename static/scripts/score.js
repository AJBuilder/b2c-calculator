
window.addEventListener("DOMContentLoaded", async () => {

    // Dynamic Score Updating
    populateScore();
    document.getElementById("factory-dropdown").addEventListener("change", populateScore);
    document.getElementById("district1-dropdown").addEventListener("change", populateScore);
    document.getElementById("district2-dropdown").addEventListener("change", populateScore);
    document.getElementById("district3-dropdown").addEventListener("change", populateScore);

    // Create the City Grid View
    const cityTable = document.getElementById("city-board-tiles");
    fillCityTable(cityTable);

});

// TODO: WRITE SCORE FUNCTION AND HELPERS
function scoreCity(){
    const cityTiles = JSON.parse(document.getElementById("city-tiles").value.replaceAll("\'", "\""));
    return {
        "shop_score":scoreShops(cityTiles),
        "park_score":scoreParks(cityTiles),
        "tavern_score":scoreTaverns(cityTiles),
        "office_score":scoreOffices(cityTiles),
        "house_score":scoreHouses(cityTiles),
        "civic_score":scoreCivics(cityTiles)
    };
}

function scoreShops(cityTiles){
    return 0;
}
function scoreParks(cityTiles){
    return 0;
}
function scoreTaverns(cityTiles){
    return 0;
}
function scoreOffices(cityTiles){
    return 0;
}
function scoreHouses(cityTiles){
    return 0;
}
function scoreCivics(cityTiles){
    return 0;
}
function countFactories(cityTiles){
    return 0;
}

// populates score changes through the frontend
function populateScore(){

    const scores = scoreCity();
    const cityTiles = JSON.parse(document.getElementById("city-tiles").value.replaceAll("\'", "\""));
    const numFactories = countFactories(cityTiles);

    document.getElementById("district1-score").innerText = document.getElementById("district1-dropdown").value;
    document.getElementById("district2-score").innerText = document.getElementById("district2-dropdown").value;
    document.getElementById("district3-score").innerText = document.getElementById("district3-dropdown").value;

    document.getElementById("shop-score").innerText = scores.shop_score;
    document.getElementById("factory-score").innerText = numFactories * Number(document.getElementById("factory-dropdown").value);
    document.getElementById("park-score").innerText = scores.park_score;
    document.getElementById("office-score").innerText = scores.office_score;
    document.getElementById("tavern-score").innerText = scores.tavern_score;
    document.getElementById("house-score").innerText = scores.house_score;
    document.getElementById("civic-score").innerText = scores.civic_score;

    let total = (numFactories * Number(document.getElementById("factory-dropdown").value));
    total += scores.shop_score;
    total += scores.park_score;
    total += scores.office_score;
    total += scores.tavern_score;
    total += scores.house_score;
    total += scores.civic_score;
    total += Number(document.getElementById("district1-dropdown").value);
    total += Number(document.getElementById("district2-dropdown").value);
    total += Number(document.getElementById("district3-dropdown").value);
    document.getElementById("total-score-box").innerText = total;
    document.getElementById("total-score-heading").innerText = total;
}

// Functions to fill in the city tile grid
function fillCityTable(cityTable){
    for(let i = 0; i < 5; i++){
        cityTable.appendChild(makeTR());
    }
}

function makeTR(){
    const tr = document.createElement("tr");
    for(let i = 0; i < 5; i++){
        tr.appendChild(makeTD());
    }
    return tr;
}

function makeTD(){
    const options = [
        "empty", 
        "factory", 
        "shop", 
        "park", 
        "office", 
        "tavern", 
        "house", 
        "civic", 
        "vertical_bridge",
        "horozontal_bridge"
    ];

    const td = document.createElement("td");
    const td_dropdown = document.createElement("select");
    for(const op of options){
        const option = document.createElement("option");
        option.innerText = op;
        option.value = op;
        td_dropdown.appendChild(option);
    }
    td_dropdown.addEventListener("change", () => {
        const tile = td_dropdown.value;
        td_dropdown.style.backgroundColor = "transparent";
        td_dropdown.style.background = `/static/icons/${tile}_icon.png`;
        populateScore();
    });
    td.appendChild(td_dropdown);
    return td;
}