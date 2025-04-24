const loader = document.getElementById("loading_results");
const subMidi = document.getElementById("submit_midi");
const inputLabel = document.getElementById("midi_input_label");
const midiInput = document.getElementById("midi_file");


subMidi.addEventListener("click", () => {
    loader.classList.remove("hidden");
})

midiInput.addEventListener("change", () => {
    inputLabel.textContent = "Upload Different File";
    subMidi.disabled = false;
})