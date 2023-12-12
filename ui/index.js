function bytesToBase64(bytes) {
  const binString = String.fromCodePoint(...bytes);
  return btoa(binString);
}

const url = 'http://34.41.169.38/';
const chunk_size = 1;

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
      slice = chunk_size * (audioChunks.length - 1);
      user = document.getElementById("uname").value + "_" + slice;
      ans = JSON.stringify({mp3:btoa(event.data.text), filename:user})
      console.log(ans)
      upload_url = url + "upload";
      fetch(
        upload_url,
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

    const start = () => mediaRecorder.start(chunk_size*1000);

    const stop = () => mediaRecorder.stop();

    resolve({ start, stop });
  });

const sleep = time => new Promise(resolve => setTimeout(resolve, time));


function makeid(length) {
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}

const handleStart = async () => {
  const recorder = await recordAudio();
  const start = document.getElementById("start");
  const stop = document.getElementById("stop");
  const textbox = document.getElementById("uname");
  start.disabled = true;
  if (textbox.value == '') {
    textbox.value = makeid(5);
  }
  textbox.disabled = true;
  recorder.start();
  stop.addEventListener("click", stop => {
    recorder.stop();
    start.disabled=false;
  });
};

