

window.addEventListener("DOMContentLoaded", async () => {

    // const scorebtn = document.getElementById("image-submit");
    // scorebtn.addEventListener("click", populateScore);

    // District Collapsible Element
    const districts = document.getElementById("district-collapsible");
    districts.addEventListener("click", () => {
        const dropdowns = document.getElementById("district-scoring");
        if (dropdowns.style.display === "block"){
            dropdowns.style.display = "none"
        } else {
            dropdowns.style.display = "block"
        }
    });

    // Display Image after taken
    document.getElementById("image-input").addEventListener("change", function(event) {
        const file = event.target.files[0]; // Get the uploaded file
        if (file) {
            const reader = new FileReader();
    
            reader.onload = function(e) {
                const imageLabel = document.getElementById("image-input-label");
                imageLabel.style.backgroundImage = "none"; // Remove the camera icon
                imageLabel.style.height = "90vw"; // Resize the photo to be bigger
                imageLabel.style.width = "90vw";
                imageLabel.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`; // Display image
            };
    
            reader.readAsDataURL(file); // Convert file to base64 string
        }
    });

    // Create the City Grid View
    const cityTable = document.getElementById("city-board-tiles");
    fillCityTable(cityTable);

});

function populateScore(){
    // fill the score area
    // add in district score
    // add in factory score
}

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
    const options = ["empty", "factory", "shop", "park", "office", "tavern", "house", "civic", "bridge"]
    const td = document.createElement("td");
    const td_dropdown = document.createElement("select");
    for(const op of options){
        const option = document.createElement("option");
        option.innerText = op;
        option.value = op
        td_dropdown.appendChild(option);
    }
    td_dropdown.addEventListener("change", () => {
        const tile = td_dropdown.value;
        td_dropdown.style.backgroundColor = changeTile(tile);
        console.log("tile")
    });
    td.appendChild(td_dropdown);
    return td;
}

function changeTile(value){
        const backgroundColors = new Map([
        ["shop", "#fcba03"],
        ["factory", "#706f6c"],
        ["park", "#1a5721"],
        ["office", "#082f73"],
        ["tavern", "#bd0d13"],
        ["house", "#3b1c1d"],
        ["civic", "#360769"],
        ["empty", "#f8f8f8"],
        ["bridge", "#161617"]
    ]);
    return backgroundColors.get(value) ?? "#f8f8f8";
}