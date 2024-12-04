let pyodideReady = false; // Tracks if Pyodide is ready
let pyodide = null;       // Holds the Pyodide instance


// Load a Python file into Pyodide's virtual filesystem
async function loadPythonFile(filePath, targetPath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${filePath}`);
        }
        const fileCode = await response.text();
        pyodide.FS.writeFile(targetPath, fileCode);
        console.log(`${filePath} loaded into Pyodide as ${targetPath}.`);
    } catch (error) {
        console.error(`Error loading ${filePath}:`, error);
    }
}

// Load the `functions` folder into Pyodide
async function loadFunctionsFolder(pyodide) {
    try {
        // Create the `functions` folder in Pyodide's filesystem
        pyodide.FS.mkdir("functions");

        // List of files in the `functions` folder
        const functionFiles = [
            "functions/download.py",
            "functions/soni_functions.py",
            "functions/make_midi.py",
        ];

        // Load each file into the Pyodide filesystem
        for (const file of functionFiles) {
            await loadPythonFile(file, file);
        }
        console.log("All functions loaded successfully.");
    } catch (error) {
        console.error("Error loading functions folder:", error);
    }
}

// Load my_midiutil.py into Pyodide
async function loadMidiUtil(pyodide) {
    await loadPythonFile("my_midiutil.py", "my_midiutil.py");
}

// Load main.py into Pyodide
async function loadMain(pyodide) {
    await loadPythonFile("main.py", "main.py");
}

// Load Pyodide and required Python packages
async function loadPyodideAndPackages() {
    try {
        pyodide = await loadPyodide(); // Load Pyodide
        console.log("Pyodide loaded.");

        // Load pre-bundled packages
        await pyodide.loadPackage("micropip");
        console.log("micropip package loaded.");

        // Install Python packages via micropip
        await pyodide.runPythonAsync(`
            import micropip
            await micropip.install('matplotlib')
            await micropip.install('pandas')
        `);
        console.log("matplotlib installed successfully.");

        await pyodide.loadPackage("pandas");
        await pyodide.loadPackage("matplotlib");

        pyodideReady = true; // Mark as ready
        console.log("Pyodide and packages are ready.");
    } catch (error) {
        console.error("Error loading Pyodide or packages:", error);
    }
}

// Check if the loaded Python files can be imported
async function testPythonImports() {
    try {
        await pyodide.runPythonAsync(`
            import sys
            sys.path.append('.')  # Add current directory to sys.path
            print("Testing import of Python modules...")
            try:
                import my_midiutil
                print("Successfully imported my_midiutil!")
            except Exception as e:
                print(f"Error importing my_midiutil: {e}")

            try:
                from functions.download import download_files
                print("Successfully imported download_files from functions.download!")
            except Exception as e:
                print(f"Error importing from functions.download: {e}")

            try:
                import main
                print("Successfully imported main!")
            except Exception as e:
                print(f"Error importing main: {e}")
        `);
    } catch (error) {
        console.error("Error testing Python imports:", error);
    }
}

// Load .txt file with weatherdata
async function loadTxt(pyodide) {
    try {
        // Create the `weatherdata` folder in Pyodide's filesystem
        pyodide.FS.mkdir("weatherdata");

        // List of files in the `weatherdata` folder
        const functionFiles = [
            "weatherdata/OF_wetterpark_zehn_min_tu_20200101_20211231_07341.txt"
        ];

        // Load each file into the Pyodide filesystem
        for (const file of functionFiles) {
            await loadPythonFile(file, file);
        }
        console.log("All data loaded successfully.");
    } catch (error) {
        console.error("Error loading weatherdata folder:", error);
    }
}

// Generate MIDI file using main.py
async function generateMedia(startDate, endDate, bpm) {
    try {
        console.log("Generating MIDI file...");
        const midiPath = await pyodide.runPythonAsync(`
            try: 
                from main import generate_media
                import io
                import json
                print("${startDate}")
                print("${endDate}")
                generate_media("${startDate}", "${endDate}", int(${bpm}))
            except Exception as e:
                print(f"Error occurred: {e}")
                raise
        `);
        console.log("MIDI generated at:", midiPath);

        // Parse the JSON result
        const { audioFile, video1, video2 } = JSON.parse(midiPath);
        console.log("Media generated:", { audioFile, video1, video2 });

        // Fetch and log the audio file
        const audioData = pyodide.FS.readFile(audioFile);
        console.log("Audio file content:", audioData);
        
        // ABFUCK
        // Fetch and log the video placeholders
        const video1Data = pyodide.FS.readFile(video1);
        const video2Data = pyodide.FS.readFile(video2);
        console.log("Video 1 content:", video1Data);
        console.log("Video 2 content:", video2Data);

        return { audioFile, video1, video2 };
    } catch (error) {
        console.error("Error generating media:", error);
        throw error;
    }
}

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

    if (!startDate || !endDate || !bpm) {
        alert("Please fill out all fields!");
        return;
    }

    try {
        console.log("Loading Python files...");
        await loadMidiUtil(pyodide);
        await loadFunctionsFolder(pyodide); // Load the functions folder
        await loadMain(pyodide);
        await loadTxt(pyodide);
        console.log("Loading data in pyodide");
        //await pyodide.runPythonAsync(`
        //    # Datei im virtuellen Dateisystem öffnen und lesen
        //    with open("weatherdata/OF_wetterpark_zehn_min_tu_20200101_20211231_07341.txt", "r") as file:
        //        content = file.read()
        //        print("Inhalt der Datei:", content)
        //`);

        console.log("Testing Python imports...");
        await testPythonImports();

        console.log("Generating Media...");
        const { audioFile, video1, video2 } = await generateMedia(startDate, endDate, bpm);

        console.log("Fetching MIDI data...");
        const midiData = pyodide.FS.readFile(audioFile);

        console.log("Creating MIDI download...");
        const audioBlob = new Blob([midiData], { type: "audio/midi" });
        const audioUrl = URL.createObjectURL(audioBlob);

        const audioPlayer = document.getElementById("audio-player");
        audioPlayer.src = audioUrl;

        console.log("Fetching video placeholders...");
        const video1Data = pyodide.FS.readFile(video1);
        const video2Data = pyodide.FS.readFile(video2);

        console.log("Video placeholders fetched:");
        console.log("Video 1 data length:", video1Data.length);
        console.log("Video 2 data length:", video2Data.length);

        alert("Audio and videos generated successfully!");
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while generating content.");
    }
});

// Initialize Pyodide when the page loads
window.addEventListener("load", () => {
    loadPyodideAndPackages();
});
