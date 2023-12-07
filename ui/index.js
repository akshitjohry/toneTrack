const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      console.log("New event!!!");
      audioChunks.push(event.data);
      console.log(event.data.text);
      console.log(event.data);


      fetch(
        'https://34.120.17.11/separate',
        {
          method: 'POST',
          data: {
            'recording': btoa(event.data.text)
          }
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

