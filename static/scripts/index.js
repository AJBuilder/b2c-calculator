window.addEventListener("DOMContentLoaded", async () => {

    // District Collapsible Element
    document.getElementById("district-collapsible").addEventListener("click", () => {
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
                imageLabel.style.height = "90vw"; // Resize the photo to be bigger than the camera icon was
                imageLabel.style.width = "90vw";
                imageLabel.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
                document.getElementById("image-submit").style.backgroundColor = "red";
            };
            reader.readAsDataURL(file);
        }
    });

    // Remove Image and Image Capture when Scored or remove score area if not scored
    const scored = document.getElementById("scored").value;
    if(scored === "True"){
        document.getElementById("page-container").removeChild(document.getElementById("image-upload"));
    } else {
        document.getElementById("page-container").removeChild(document.getElementById("score-area"));
    }

    // ============================
    // Toggle custom input fields for district dropdowns
    // ============================
    const dropdowns = document.querySelectorAll("#district-scoring select");

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("change", () => {
            const customInputId = dropdown.id.replace("dropdown", "custom");
            const customInput = document.getElementById(customInputId);

            if (dropdown.value === "custom") {
                customInput.style.display = "inline-block";
            } else {
                if (customInput) {
                    customInput.style.display = "none";
                    customInput.value = "";
                }
            }
        });
    });

});
