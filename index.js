const loader = document.getElementById("loading_results");
const subMidi = document.getElementById("submit_midi");
console.log(loader);
console.log(subMidi);
subMidi.addEventListener("click", () => {
    console.log("heard")
    loader.classList.remove("hidden");
})