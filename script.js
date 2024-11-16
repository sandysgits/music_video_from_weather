document.getElementById("start-button").addEventListener("click", async () => {
    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const bpm = document.getElementById("bpm").value;

    if (!startDate || !endDate || !bpm) {
        alert("Please fill out all fields!");
        return;
    }

    try {
        const response = await fetch('/run-python', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ startDate, endDate, bpm }),
        });

        const data = await response.json();
        document.getElementById("audio-player").src = `assets/audio/${data.audioFile}`;
        document.getElementById("graphic-1").innerHTML = `<video src="assets/video/${data.video1}" controls></video>`;
        document.getElementById("graphic-2").innerHTML = `<video src="assets/video/${data.video2}" controls></video>`;
    } catch (error) {
        console.error("Error:", error);
    }
});
