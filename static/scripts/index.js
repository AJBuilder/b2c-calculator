

window.addEventListener("DOMContentLoaded", async () => {

    const districts = document.getElementById("district-collapsible");
    districts.addEventListener("click", () => {
        const dropdowns = document.getElementById("district-scoring");
        if (dropdowns.style.display === "block"){
            dropdowns.style.display = "none"
        } else {
            dropdowns.style.display = "block"
        }
    });

    document.getElementById("image-input").addEventListener("change", function(event) {
        const file = event.target.files[0]; // Get the uploaded file
        if (file) {
            const reader = new FileReader();
    
            reader.onload = function(e) {
                const imageLabel = document.getElementById("image-input-label");
                imageLabel.style.backgroundImage = "none"; // Remove the camera icon
                imageLabel.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`; // Display image
            };
    
            reader.readAsDataURL(file); // Convert file to base64 string
        }
    });

});
