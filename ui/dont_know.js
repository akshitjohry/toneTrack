const recordAudioAndSend = (apiEndpoint, onChunkRecorded) =>
  new Promise(async (resolve, reject) => {
    console.log("In record and send");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      let recording = false;
      console.log("Event listener");

      mediaRecorder.addEventListener("dataavailable", async (event) => {
        if (event.data.size > 0) {
          const audioBlob = new Blob([event.data], { type: "audio/mpeg" });
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);

          if (onChunkRecorded && typeof onChunkRecorded === "function") {
            // Call the callback with the audio-related data for each chunk
            // onChunkRecorded({ audioBlob, audioUrl, audio });
            onChunkRecorded({ audioBlob, audioUrl, audio });

          }
        }
      });

      const start = () => {
        console.log("Event start");
        if (!recording) {
          recording = true;
          mediaRecorder.start();
        }
      };

      const stop = () =>
        new Promise(async (resolve) => {
          console.log("Event stop");
          if (recording) {
            recording = false;

            mediaRecorder.addEventListener("stop", async () => {
              // Stop the tracks of the media streamm
              stream.getTracks().forEach((track) => track.stop());

              // Resolve the promise with the final audio data
              resolve();
            });

            mediaRecorder.stop();
          }
        });

      resolve({ start, stop });
    } catch (error) {
      reject(error);
    }
  });

const sleep = (time) => new Promise((resolve) => setTimeout(resolve, time));

const handleStart = async () => {
  try {
    console.log("Starting the recording");
    const apiEndpoint = "https://example.com/upload-audio"; // Replace with your API endpoint
    const startButton = document.getElementById("start");
    const stopButton = document.getElementById("stop");

    startButton.disabled = true;
    stopButton.disabled = false;

    let chunksRecorded = 0;
    // const maxChunks = 4; // Change this to the desired number of chunks (e.g., 15s * 4 = 1 minute)
    const chunkDuration = 1500; // 15 seconds in milliseconds

    const onChunkRecorded = async ({ audioBlob, audioUrl, audio }) => {
      // Send the current chunk to the API
      const formData = new FormData();
      formData.append("audio", audioBlob, `recording_chunk_${chunksRecorded}.mp3`);
      console.log(formData);
      try {
        console.log("Sending files to url: ", apiEndpoint);
        // const response = await fetch(apiEndpoint, {
        //   method: "POST",
        //   body: formData,
        // });
        // if (!response.ok) {
        //   throw new Error("Failed to send audio to the API");
        // }
      } catch (error) {
        console.error("Error sending chunk to API: ", error);
      }

      // Play the current chunk
      // audio.play();

      // Increment the count of recorded chunks
      console.log("Chunk count inc");
      chunksRecorded++;
    };

    console.log("Before record and send");
    const recorder = await recordAudioAndSend(apiEndpoint, onChunkRecorded);
    recorder.start();

    // Record in chunks of 15 seconds until the stop button is pressed
    // while (recorder.isRecording()) {
    //   console.log("Sleeping");
    //   await sleep(chunkDuration);
    // }
  } catch (error) {
    console.error("Error: ", error);
  }
};

const handleStop = async () => {
  const startButton = document.getElementById("start");
  const stopButton = document.getElementById("stop");

  startButton.disabled = false;
  stopButton.disabled = true;
  
  const recorder = await recordAudioAndSend("", "onChunkRecorded");
  await recorder.stop();
};