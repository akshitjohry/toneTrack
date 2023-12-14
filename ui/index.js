
function bytesToBase64(bytes) {
  const binString = String.fromCodePoint(...bytes);
  return btoa(binString);
}

const url = 'http://104.197.35.240/';
const chunk_size = 20;
let slice = 0;
let audioChunks = [];
let recordingInterval;

const recordAudio = () =>
  new Promise(async (resolve) => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.addEventListener('dataavailable', (event) => {
      console.log('New event!!!');
      audioChunks.push(event.data);
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);

      reader.onloadend = async () => {
        const base64data = reader.result.split(',')[1];
        const user = document.getElementById('uname').value + '_' + slice;
        const ans = JSON.stringify({ mp3: base64data, filename: user });
        console.log(user);

        const upload_url = url + 'upload';
        await fetch(upload_url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: ans,
        });

        slice += chunk_size;
        audioChunks = [];
      };
    });

    const start = () => {
      mediaRecorder.start(chunk_size * 1000);
      recordingInterval = setInterval(() => {
        mediaRecorder.stop();
        mediaRecorder.start(chunk_size * 1000);
      }, chunk_size * 1000);
    };

    const stop = () => {
      mediaRecorder.stop();
      clearInterval(recordingInterval);
    };

    resolve({ start, stop });
  });

const sleep = (time) => new Promise((resolve) => setTimeout(resolve, time));

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
  const startButton = document.getElementById('start');
  const stopButton = document.getElementById('stop');
  const textbox = document.getElementById('uname');
  startButton.disabled = true;

  if (textbox.value === '') {
    textbox.value = makeid(5);
  }
  textbox.disabled = true;

  recorder.start();

  stopButton.addEventListener('click', () => {
    recorder.stop();
    startButton.disabled = false;
  });
};

