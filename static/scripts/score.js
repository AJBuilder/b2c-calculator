
window.addEventListener("DOMContentLoaded", async () => {
    const scored = document.getElementById("scored").value;

    if(scored === "True"){
        // Create the City Grid View
        fillCityTable();

        // Dynamic Score Updating
        populateScore();
        document.getElementById("factory-dropdown").addEventListener("change", populateScore);
        document.getElementById("district1-dropdown").addEventListener("change", populateScore);
        document.getElementById("district2-dropdown").addEventListener("change", populateScore);
        document.getElementById("district3-dropdown").addEventListener("change", populateScore);
    }

});

// TODO: WRITE SCORE FUNCTION HELPERS
function scoreCity(cityTiles){
    return {
        "factory_score": scoreFactories(cityTiles),
        "shop_score": scoreShops(cityTiles),
        "park_score": scoreParks(cityTiles),
        "tavern_score": scoreTaverns(cityTiles),
        "office_score": scoreOffices(cityTiles),
        "house_score": scoreHouses(cityTiles),
        "civic_score": scoreCivics(cityTiles)
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
function scoreFactories(cityTiles){
    return 0;
}

// populates score changes through the frontend
function populateScore(){
    const cityTiles = getCityTiles();

    console.log(cityTiles);

    const scores = scoreCity(cityTiles);

    document.getElementById("district1-score").innerText = document.getElementById("district1-dropdown").value;
    document.getElementById("district2-score").innerText = document.getElementById("district2-dropdown").value;
    document.getElementById("district3-score").innerText = document.getElementById("district3-dropdown").value;

    document.getElementById("shop-score").innerText = scores.shop_score;
    document.getElementById("factory-score").innerText = scores.factory_score;
    document.getElementById("park-score").innerText = scores.park_score;
    document.getElementById("office-score").innerText = scores.office_score;
    document.getElementById("tavern-score").innerText = scores.tavern_score;
    document.getElementById("house-score").innerText = scores.house_score;
    document.getElementById("civic-score").innerText = scores.civic_score;

    total = scores.factory_score;
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
function fillCityTable(){
    const cityTable = document.getElementById("city-board-tiles");
    const cityTiles = JSON.parse(document.getElementById("city-tiles").value.replaceAll("\'", "\""));

    for(const cityRow of cityTiles){
        cityTable.appendChild(makeTR(cityRow));
    }
}

function makeTR(cityRow){
    const tr = document.createElement("tr");
    for(const cityTile of cityRow){
        tr.appendChild(makeTD(cityTile));
    }
    return tr;
}

// TODO: REWRITE THIS FUNCTION
function makeTD(cityTile){
    const options = [ 
        "factory", 
        "shop", 
        "park", 
        "tavern",
        "office",  
        "house", 
        "civic", 
        "empty",
        "bridge"
    ];

    const td = document.createElement("td"); // create table data (cell)

    // hidden field to track what tile is here for rescoring on change
    const hiddenID = document.createElement("input");
    hiddenID.type = "hidden";
    hiddenID.value = cityTile;
    td.appendChild(hiddenID);

    const td_dropdown = document.createElement("select"); // create dropdown

    // fill dropdown options
    for(const op of options){
        const option = document.createElement("option");
        option.innerText = op;
        option.value = op;
        td_dropdown.appendChild(option);
    }
    td_dropdown.value = cityTile.split(" ")[0]; // fill selected option
    td.appendChild(td_dropdown); // attach dropdown to table cell
    
    fillIcon(td_dropdown.value, td); // fill table cell icon

    // Change the tile when the dropdown is changed
    td_dropdown.addEventListener("change", () => {
        const firstChildHiddenID = td.firstChild; // get the identification of the td
        const secondChildDropdown = td.children[1]; // get the dropdown so it stays
        const thirdChildImg = td.children[2]; // get the first img to overwrite it

        // Remove all children except the dropdown and the base img
        for(const child of td.children){
            if(child !== td.firstChild && child !== secondChildDropdown && child !== thirdChildImg){
                td.remove(child)
            }
        }

        const tileType = td_dropdown.value; // find what the dropdown changed to
        thirdChildImg.src = `/static/icons/${tileType}_icon.png`; // change the base image

        //TODO: if tileType is tavern, civic, empty/landscape, bridge change the overlay images
        if(tileType === "tavern"){
            // TODO: figure out tavern type
            // TODO: overlay proper tavern icon
            firstChildHiddenID.value = `${tileType}`; // update the hidden field
        } else if(tileType === "civic"){
            // TODO: figure out civic type
            // TODO: overlay civic bonuses
            firstChildHiddenID.value = `${tileType}`; // update the hidden field
        } else if(tileType === "bridge"){
            // TODO: figure out bridge direction
            // TODO: get correct img
            firstChildHiddenID.value = `${tileType}`; // update the hidden field
        } else {
            firstChildHiddenID.value = tileType; // update the hidden field
        }

        populateScore(); // recalculate the score
    });
    return td;
}

function fillIcon(tile, td){
    tile = tile.split(" ");
    if(tile[0] === "tavern"){

    } else if(tile[0] === "civic"){

    } else {
        const img = document.createElement("img");
        img.src = `/static/icons/${tile[0]}_icon.png`;
        td.appendChild(img);
    }
}

function getCityTiles(){
    // TODO: get the city tiles from the hidden inputs in the tds
    let cityTiles = [];

    const table = document.getElementById("city-board-tiles");
    for(tableRow of table.children){
        let tr = [];
        for(tableData of tableRow.children){
            tr.push(tableData.firstChild.value);
        }
        cityTiles.push(tr);
    }
    return cityTiles;
}