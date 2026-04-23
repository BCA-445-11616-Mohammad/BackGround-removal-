// 🔹 existing (agar use kar raha hai)
const form = document.querySelector("form");
const loader = document.getElementById("loader");

if (form && loader) {
    form.addEventListener("submit", () => {
        loader.style.display = "flex";
    });
}

// 🔹 menu toggle (safe)
function toggleMenu() {
    let menu = document.getElementById("sideMenu");

    if (menu.style.left === "0px") {
        menu.style.left = "-260px";
    } else {
        menu.style.left = "0px";
    }
}

// 🔥 PDF upload system
const input = document.getElementById("pdfInput");
const fileList = document.getElementById("fileList");
const addMoreBtn = document.getElementById("addMoreBtn");

let allFiles = []; // 🔥 important (store all files)

// 📂 initial select
input.addEventListener("change", function () {
    handleFiles(input.files);
});

// ➕ add more button
addMoreBtn.addEventListener("click", () => {
    input.click();
});

// 📦 handle files
function handleFiles(files) {

    for (let i = 0; i < files.length; i++) {
        allFiles.push(files[i]); // 🔥 append
    }

    showFiles();
    

    // show button only after 1 file
    if (allFiles.length > 0) {
        addMoreBtn.style.display = "inline-block";
        document.getElementById("mergeBtn").style.display = "inline-block";
    }
}

// 📦 show files
function showFiles() {
    fileList.innerHTML = "";

    allFiles.forEach(file => {
        const div = document.createElement("div");
        div.className = "file-card";

        div.innerHTML = `
            <img src="https://cdn-icons-png.flaticon.com/512/337/337946.png" width="40">
            <p>${file.name}</p>
        `;

        fileList.appendChild(div);
    });
const form = document.querySelector("form");


}

form.addEventListener("submit", function(e) {
    e.preventDefault();

    const formData = new FormData();

    // 🔥 DEBUG (yahan hona chahiye)
    console.log("submitting files:", allFiles);

    allFiles.forEach(file => {
        formData.append("pdfs", file);
    });

    fetch("/merge-pdf", {
        method: "POST",
        body: formData
    })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        window.open(url);
    });
});