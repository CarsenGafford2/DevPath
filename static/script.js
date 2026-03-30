
// Get form element
const form = document.getElementById("projectForm");

// Run only if form exists
if (form) {

    form.addEventListener("submit", function (event) {

        const selects = form.querySelectorAll("select");
        let isValid = true;

        // Check if all fields are filled
        selects.forEach(function (select) {
            if (!select.value) {
                isValid = false;
            }
        });

        // Prevent submission if invalid
        if (!isValid) {
            event.preventDefault();
            alert("Please fill all fields before submitting");
            return;
        }

        // Show loading state
        const button = form.querySelector("button");
        button.innerText = "Generating...";
        button.disabled = true;
    });
}
