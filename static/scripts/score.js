
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

function scoreShops(cityTiles) {
    const SCORES = [0, 2, 5, 10, 15, 20];
    const rows = cityTiles.length;
    const cols = cityTiles[0].length;
    let used = new Set();
    let totalScore = 0;

    function getKey(i, j) {
        return `${i},${j}`;
    }

    function collectLines() {
        const lines = [];

        // Horizontal lines
        for (let i = 0; i < rows; i++) {
            let j = 0;
            while (j < cols) {
                if (cityTiles[i][j] === "shop") {
                    let start = j;
                    while (j < cols && cityTiles[i][j] === "shop") j++;
                    let length = j - start;
                    let coords = [];
                    for (let k = start; k < j; k++) {
                        coords.push([i, k]);
                    }
                    lines.push({ length, coords, isVertical: false });
                } else {
                    j++;
                }
            }
        }

        // Vertical lines
        for (let j = 0; j < cols; j++) {
            let i = 0;
            while (i < rows) {
                if (cityTiles[i][j] === "shop") {
                    let start = i;
                    while (i < rows && cityTiles[i][j] === "shop") i++;
                    let length = i - start;
                    let coords = [];
                    for (let k = start; k < i; k++) {
                        coords.push([k, j]);
                    }
                    lines.push({ length, coords, isVertical: true });
                } else {
                    i++;
                }
            }
        }

        return lines;
    }

    const allLines = collectLines();

    // Score and sort lines descending by score
    allLines.sort((a, b) => {
        const scoreA = SCORES[Math.min(a.length, 5)];
        const scoreB = SCORES[Math.min(b.length, 5)];
        return scoreB - scoreA;
    });

    for (const line of allLines) {
        // Skip if any tile already used
        if (line.coords.some(([i, j]) => used.has(getKey(i, j)))) continue;

        // Score the line
        totalScore += SCORES[Math.min(line.length, 5)];

        // Mark tiles as used
        for (const [i, j] of line.coords) {
            used.add(getKey(i, j));
        }
    }

    return totalScore;
}



function scoreParks(cityTiles) {
    const visited = Array.from({ length: 5 }, () => Array(5).fill(false));

    function inBounds(x, y) {
        return x >= 0 && x < 5 && y >= 0 && y < 5;
    }

    function getNeighbors(x, y) {
        const deltas = [[0,1], [1,0], [0,-1], [-1,0]];
        return deltas
            .map(([dx, dy]) => [x + dx, y + dy])
            .filter(([nx, ny]) => inBounds(nx, ny));
    }

    function dfs(x, y) {
        const stack = [[x, y]];
        let size = 0;

        while (stack.length > 0) {
            const [cx, cy] = stack.pop();
            if (!inBounds(cx, cy) || visited[cx][cy] || cityTiles[cx][cy] !== "park") continue;
            visited[cx][cy] = true;
            size += 1;
            stack.push(...getNeighbors(cx, cy));
        }

        return size;
    }

    function parkScore(size) {
        if (size === 0) return 0;
        if (size === 1) return 2;
        if (size === 2) return 8;
        if (size === 3) return 12;
        return 12 + (size - 3);
    }

    let totalScore = 0;

    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            if (cityTiles[i][j] === "park" && !visited[i][j]) {
                const size = dfs(i, j);
                totalScore += parkScore(size);
            }
        }
    }

    return totalScore;
}
function scoreTaverns(cityTiles){
    const SCORES = [0,1,4,9,17];
    let tavern_score = 0;
    let tavern_map = {
        "inn":0,
        "bar":0,
        "music":0,
        "restaurant":0
    };
    for(let i = 0; i < cityTiles.length; i++){
        for(let j = 0; j < cityTiles[i].length; j++){
            if(cityTiles[i][j].split(" ")[0] === "tavern"){
                tavern_map[cityTiles[i][j].split(" ")[1]] += 1
            }
        }
    }
    while(true){
        let num_dif_types = 0;
        for(const tavern_type in tavern_map){
            if(tavern_map[tavern_type] > 0){
                num_dif_types += 1;
                tavern_map[tavern_type] -= 1;
            }
        }
        if(num_dif_types === 0){
            break;
        }
        tavern_score += SCORES[num_dif_types];
        num_dif_types = 0;
    }
    console.log(tavern_score);
    return tavern_score;
}
function scoreOffices(cityTiles){
    const SCORES = [0,1,3,6,10,15,21,22,24,27,31,36,42,43,45,48,52,57,63,64,66];
    let office_count = 0;
    let office_score = 0;
    for(let i = 0; i < cityTiles.length; i++){
        for(let j = 0; j < cityTiles[i].length; j++){
            if(cityTiles[i][j] === "office"){
                office_count += 1;
                for(let neighbor of getNeighbors(i,j,cityTiles)){
                    if(neighbor.split(" ")[0] === "tavern"){
                        office_score += 1;
                        break;
                    }
                }
            }
        }
    }
    return office_score + SCORES[office_count];
}
function scoreHouses(cityTiles){
    let houseList = ["factory", "shop", "park", "tavern", "office"];
    let numScoringHouses = 0;
    let numFactoryHouses = 0;
    for(let i = 0; i < cityTiles.length; i++){
        for(let j = 0; j < cityTiles[i].length; j++){
            if(cityTiles[i][j] === "house"){
                if(getNeighbors(i, j, cityTiles).includes("factory")){
                    numFactoryHouses += 1; // factory adjacent houses
                }else{
                    numScoringHouses += 1; // good houses
                }
            }
            if(tile.split(" ")[0] in houseList){
                houseList.remove(tile.split(" ")[0]); // how much to score each house
            }
        }
    }
    if(houseList.length === 0){ // extremly unlikely, perhaps even impossible
        return numHouses*1;
    }
    return ((numScoringHouses*houseList.length) + (numFactoryHouses));
}
function scoreCivics(cityTiles){
    let civic_total = 0;
    for(let i = 0; i < cityTiles.length; i++){
        for(let j = 0; j < cityTiles[i].length; j++){
            const tile = cityTiles[i][j];
            if(tile.split(" ")[0] === "civic"){
                let this_civic = 0;
                const b1 = tile.split(" ")[1];
                const b2 = tile.split(" ")[2];
                const neg = tile.split(" ")[3];
                const neighbors = getNeighbors(i, j, cityTiles);
                for(let neighbor of neighbors){
                    let b1_found = false;
                    let b2_found = false;
                    if(neighbor.split(" ")[0] === neg){
                        this_civic = 1;
                        break;
                    }
                    if(b1_found == false && neighbor.split(" ")[0] === b1){
                        b1_found = true;
                        this_civic += 3
                    }
                    if(b2_found == false && neighbor.split(" ")[0] === b2){
                        b2_found = true
                        this_civic += 3
                    }
                }
                if(this_civic == 0){
                    this_civic = 1;
                }
                civic_total += this_civic;
            }
        }
    }
    return civic_total;
}
function scoreFactories(cityTiles){
    const factoryValue = Number(document.getElementById("factory-dropdown").value);
    let numFactories = 0;
    for(tileRow of cityTiles){
        for(tile of tileRow){
            if(tile === "factory"){
                numFactories += 1;
            }
        }
    }
    return factoryValue * numFactories;
}

// populates score changes through the frontend
function populateScore(){
    const cityTiles = getCityTiles();
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
    
    fillIcon(cityTile, td); // fill table cell icon

    // Change the tile when the dropdown is changed
    td_dropdown.addEventListener("change", async () => {
        const firstChildHiddenID = td.firstChild; // get the identification of the td
        const secondChildDropdown = td.children[1]; // get the dropdown so it stays
        const thirdChildImg = td.children[2]; // get the first img to overwrite it

        // Remove all children except the dropdown and the base img
        for (const child of Array.from(td.children)) {
            if (child !== firstChildHiddenID && child !== secondChildDropdown && child !== thirdChildImg) {
                td.removeChild(child);
            }
        }

        const tileType = td_dropdown.value; // find what the dropdown changed to
        thirdChildImg.src = `/static/icons/${tileType}_icon.png`; // change the base image

        //if tileType is tavern, civic, or bridge pick options
        if(tileType === "tavern"){
            const type = await selectTavern();
            thirdChildImg.src = `/static/icons/${tileType}_${type}_icon.png`;
            firstChildHiddenID.value = `${tileType} ${type}`; // update the hidden field
        } else if(tileType === "civic"){
            // TODO: figure out civic type via civic modal
            // TODO: overlay civic bonuses
            const { bonus1, bonus2, negative } = await selectCivic();
            thirdChildImg.src = `/static/icons/${tileType}_icon.png`;

            const overlayImg1 = document.createElement("img");
            overlayImg1.src = `/static/icons/${bonus1}_icon.png`;
            overlayImg1.classList.add("imgOverlay");
            overlayImg1.classList.add("imgOverlay1");
            td.appendChild(overlayImg1);

            const overlayImg2 = document.createElement("img");
            overlayImg2.src = `/static/icons/${bonus2}_icon.png`;
            overlayImg2.classList.add("imgOverlay");
            overlayImg2.classList.add("imgOverlay2");
            td.appendChild(overlayImg2);

            const overlayImg3 = document.createElement("img");
            overlayImg3.src = `/static/icons/${negative}_icon.png`;
            overlayImg3.classList.add("imgOverlay");
            overlayImg3.classList.add("imgOverlay3");
            td.appendChild(overlayImg3);

            firstChildHiddenID.value = `${tileType} ${bonus1} ${bonus2} ${negative}`; // update the hidden field
        } else if(tileType === "bridge"){
            const type = await selectBridge();
            thirdChildImg.src = `/static/icons/${tileType}_${type}_icon.png`
            firstChildHiddenID.value = `${tileType} ${type}`; // update the hidden field
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
        const baseImg = document.createElement("img");
        baseImg.src = `/static/icons/${tile[0]}_${tile[1]}_icon.png`;
        baseImg.classList.add('baseImg');
        td.appendChild(baseImg);
    } else if(tile[0] === "civic"){
        const baseImg = document.createElement("img");
        baseImg.src = `/static/icons/${tile[0]}_icon.png`;
        td.appendChild(baseImg);

        const overlayImg1 = document.createElement("img");
        overlayImg1.src = `/static/icons/${tile[1]}_icon.png`;
        overlayImg1.classList.add("imgOverlay");
        overlayImg1.classList.add("imgOverlay1");
        td.appendChild(overlayImg1);

        const overlayImg2 = document.createElement("img");
        overlayImg2.src = `/static/icons/${tile[2]}_icon.png`;
        overlayImg2.classList.add("imgOverlay");
        overlayImg2.classList.add("imgOverlay2");
        td.appendChild(overlayImg2);

        const overlayImg3 = document.createElement("img");
        overlayImg3.src = `/static/icons/${tile[3]}_icon.png`;
        overlayImg3.classList.add("imgOverlay");
        overlayImg3.classList.add("imgOverlay3");
        td.appendChild(overlayImg3);

    } else if(tile[0] === "bridge"){
        const baseImg = document.createElement("img");
        baseImg.src = `/static/icons/${tile[0]}_${tile[1]}_icon.png`;
        td.appendChild(baseImg);
    } else {
        const baseImg = document.createElement("img");
        baseImg.src = `/static/icons/${tile[0]}_icon.png`;
        td.appendChild(baseImg);
    }
}

function selectTavern() {
    return new Promise(resolve => {
        document.getElementById("tavern-modal").style.display = "block";
        const radios = document.querySelectorAll('input[name="tavern"]');

        function handler(event) {
            const selectedValue = event.target.value;
            document.getElementById("tavern-modal").style.display = "none";

            // Clean up event listeners
            radios.forEach(r => r.removeEventListener('change', handler));

            resolve(selectedValue); // Return the selected value
        }
        radios.forEach(r => r.addEventListener('change', handler));
    });
}

function selectCivic() {
    return new Promise(resolve => {
        const modal = document.getElementById("civic-modal");
        const confirmBtn = document.getElementById("civic-confirm-btn");

        modal.style.display = "block";

        function handleConfirm() {
            const bonus1 = document.getElementById("civic-bonus1-dropdown").value;
            const bonus2 = document.getElementById("civic-bonus2-dropdown").value;
            const negative = document.getElementById("civic-negative-dropdown").value;

            modal.style.display = "none";

            confirmBtn.removeEventListener("click", handleConfirm);

            resolve({ bonus1, bonus2, negative });
        }

        confirmBtn.addEventListener("click", handleConfirm);
    });
}

function selectBridge(){
    return new Promise(resolve => {
        document.getElementById("bridge-modal").style.display = "block";
        const radios = document.querySelectorAll('input[name="bridge"]');

        function handler(event) {
            const selectedValue = event.target.value;
            document.getElementById("bridge-modal").style.display = "none";

            // Clean up event listeners
            radios.forEach(r => r.removeEventListener('change', handler));

            resolve(selectedValue); // Return the selected value
        }
        radios.forEach(r => r.addEventListener('change', handler));
    });
}

function getCityTiles(){
    // get the city tiles from the hidden inputs in the tds
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

// Gets the neighbors of the tile specified at [row, col]
function getNeighbors(row, col, cityTiles){
    let neighbors = [];
    if(row-1 >= 0){
        if(cityTiles[row-1][col] === "bridge vertical"){
            neighbors.push(cityTiles[row-2][col].split(" ")[0]);
        }else{
            neighbors.push(cityTiles[row-1][col].split(" ")[0]);
        }
    }
    if(row+1 <= 4){
        if(cityTiles[row+1][col] === "bridge vertical"){
            neighbors.push(cityTiles[row+2][col].split(" ")[0]);
        }else{
            neighbors.push(cityTiles[row+1][col].split(" ")[0]);
        }    
    }
    if(col-1 >= 0){
        if(cityTiles[row][col-1] === "bridge horizontal"){
            neighbors.push(cityTiles[row][col-2].split(" ")[0]);
        }else{
            neighbors.push(cityTiles[row][col-1].split(" ")[0]);
        }    
    }
    if(col+1 <= 4){
        if(cityTiles[row][col+1] === "bridge horizontal"){
            neighbors.push(cityTiles[row][col+2].split(" ")[0]);
        }else{
            neighbors.push(cityTiles[row][col+1].split(" ")[0]);
        }    
    }
    return neighbors;
}