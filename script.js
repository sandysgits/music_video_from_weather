let pyodideReady = false; // Tracks if Pyodide is ready
let pyodide = null;       // Holds the Pyodide instance

async function loadMidiUtil(pyodide) {
    try {
        const response = await fetch("my_midiutil.py"); // Path to your my_midiutil.py file
        if (!response.ok) {
            throw new Error("Failed to fetch my_midiutil.py");
        }
        const midiutilCode = await response.text();
        pyodide.FS.writeFile("my_midiutil.py", midiutilCode);
        console.log("MIDIUtil loaded into Pyodide.");
    } catch (error) {
        console.error("Error loading MIDIUtil:", error);
    }
}

// Load Pyodide and required Python packages
async function loadPyodideAndPackages() {
    try {
        pyodide = await loadPyodide(); // Load Pyodide
        console.log("Pyodide loaded.");

        // Load pre-bundled packages
        await pyodide.loadPackage("matplotlib");
        await pyodide.loadPackage("pandas");
        console.log("Pre-bundled packages loaded successfully.");

        // Install Python packages
        await pyodide.loadPackage("micropip");
        await pyodide.runPythonAsync(`
            import micropip
            # await micropip.install('matplotlib')
            # await micropip.install('pandas')
            # await micropip.install('audiolazy')
            print("Packages installed successfully!")

        `);

        pyodideReady = true; // Mark as ready
        console.log("Pyodide and packages are ready.");
    } catch (error) {
        console.error("Error loading Pyodide or packages:", error);
    }
}

// Initialize Pyodide when the page loads
window.addEventListener("load", () => {
    loadPyodideAndPackages();
});

// Function to generate videos
async function generateVideos() {
    const canvas1 = document.getElementById("canvas1");
    const canvas2 = document.getElementById("canvas2");

    const ctx1 = canvas1.getContext("2d");
    const ctx2 = canvas2.getContext("2d");

    const recorder1 = new MediaRecorder(canvas1.captureStream());
    const recorder2 = new MediaRecorder(canvas2.captureStream());

    let video1Chunks = [];
    let video2Chunks = [];

    recorder1.ondataavailable = (event) => video1Chunks.push(event.data);
    recorder2.ondataavailable = (event) => video2Chunks.push(event.data);

    recorder1.start();
    recorder2.start();

    // Animate canvas1
    let t = 0;
    const interval1 = setInterval(() => {
        ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
        ctx1.fillStyle = `rgb(${Math.sin(t) * 128 + 128}, 100, 200)`;
        ctx1.fillRect(t % canvas1.width, 150, 50, 50);
        t += 5;
    }, 100);

    // Animate canvas2
    let y = 0;
    const interval2 = setInterval(() => {
        ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
        ctx2.beginPath();
        ctx2.arc(320, y % canvas2.height, 50, 0, 2 * Math.PI);
        ctx2.fillStyle = `rgb(100, ${Math.cos(y) * 128 + 128}, 150)`;
        ctx2.fill();
        y += 5;
    }, 100);

    // Stop recording after 10 seconds
    await new Promise((resolve) => setTimeout(resolve, 10000));
    clearInterval(interval1);
    clearInterval(interval2);
    recorder1.stop();
    recorder2.stop();

    // Process video data
    recorder1.onstop = () => {
        const videoBlob = new Blob(video1Chunks, { type: "video/webm" });
        const videoUrl = URL.createObjectURL(videoBlob);
        const videoElement = document.createElement("video");
        videoElement.src = videoUrl;
        videoElement.controls = true;
        document.getElementById("graphic-1").appendChild(videoElement);
    };

    recorder2.onstop = () => {
        const videoBlob = new Blob(video2Chunks, { type: "video/webm" });
        const videoUrl = URL.createObjectURL(videoBlob);
        const videoElement = document.createElement("video");
        videoElement.src = videoUrl;
        videoElement.controls = true;
        document.getElementById("graphic-2").appendChild(videoElement);
    };
}

// Event listener for the "Generate" button
document.getElementById("start-button").addEventListener("click", async () => {
    if (!pyodideReady) {
        alert("Pyodide is still loading. Please wait!");
        return;
    }

    const startDate = document.getElementById("start-date").value;
    const endDate = document.getElementById("end-date").value;
    const bpm = document.getElementById("bpm").value;
    console.log(startDate);

    if (!startDate || !endDate || !bpm) {
        alert("Please fill out all fields!");
        return;
    }

    try {
        console.log("load midiutil")
        // Ensure MIDIUtil is loaded
        await loadMidiUtil(pyodide);

        // Generate audio (MIDI file)
        const result = await pyodide.runPythonAsync(`
        print("Loading packages")
        from js import console
        print("imported console")
        from pyodide.ffi import to_js
        print("imported to_js")
        from my_midiutil import MIDIFile
        print("imported midifile")
        import main
        print("imported main")

        print("Imported packages")

        # Generate MIDI, video, and sync
        midi_file, video1, video2 = main.generate_media("${startDate}", "${endDate}", int(${bpm}))

        # Return as base64-encoded blobs
        def get_base64(file_path):
            with open(file_path, "rb") as file:
                return file.read().hex()

        midi_blob = get_base64(midi_file)
        video1_blob = get_base64(video1)
        video2_blob = get_base64(video2)

        console.log(to_js({"midi": midi_blob, "video1": video1_blob, "video2": video2_blob}))
    `);

        // Create a downloadable MIDI file
        const audioBlob = new Blob([result], { type: "audio/midi" });
        const audioUrl = URL.createObjectURL(audioBlob);
        const audioPlayer = document.getElementById("audio-player");
        audioPlayer.src = audioUrl;

        // Generate videos
        await generateVideos();

        alert("Audio and videos generated successfully!");
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while generating content.");
    }
});