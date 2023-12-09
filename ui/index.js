function bytesToBase64(bytes) {
  const binString = String.fromCodePoint(...bytes);
  return btoa(binString);
}

const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      console.log("New event!!!");
      audioChunks.push(event.data);
      console.log(event.data.text);
      console.log(event.data.type);
      console.log(event.data);

      ans = JSON.stringify({mp3:btoa(event.data.text), callback:{}})
      console.log(ans)

      fetch(
        'http://34.134.253.130/upload',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: ans
        }
      ).then(response => {
        console.log(response);
      });

    });

    const start = () => mediaRecorder.start(1000);

    const stop = () => mediaRecorder.stop();

    resolve({ start, stop });
  });

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

const handleStart = async () => {
  const recorder = await recordAudio();
  const start = document.getElementById("start");
  const stop = document.getElementById("stop");
  start.disabled = true;
  recorder.start();
  stop.addEventListener("click", stop => {
    recorder.stop();
    start.disabled=false;
  });
};

