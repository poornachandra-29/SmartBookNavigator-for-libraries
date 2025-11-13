// Grab elements
const scanBtn = document.querySelector(".scan-btn");
const input = document.querySelector(".search-input");
const relatedDropdown = document.getElementById("relatedBooksDropdown");
const resultsContainer = document.getElementById("resultsList"); // main results

// Main function - Navigate directly to library layout
async function scanBook() {
    const query = input.value.trim();
    if (!query) {
        alert("Please enter a book name");
        return;
    }

    // Navigate directly to demo.html (library layout) with the book query
    window.location.href = `floor.html?title=${encodeURIComponent(query)}`;
}

// Event listeners
scanBtn.addEventListener("click", scanBook);       // button click - navigate to library layout
// Removed input event listener - only navigate when scan button is clicked

// Hide dropdown when clicking outside
document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !relatedDropdown.contains(e.target)) {
        relatedDropdown.style.display = "none";
    }
});


const aiBtn = document.querySelector(".ai-btn");

aiBtn.addEventListener("click", async () => {
    try {
        const res = await fetch("/api/ai-recommend");
        const data = await res.json();

        if (data.recommended) {
            // Save books to localStorage for next page
            localStorage.setItem("recommendedBooks", JSON.stringify(data.recommended));
            
            // Redirect to AI Recommend page
            window.location.href = "ai_recommend.html";
        } else {
            alert("No recommendations found.");
        }
    } catch (err) {
        console.error(err);
        alert("Failed to fetch recommendations.");
    }
});