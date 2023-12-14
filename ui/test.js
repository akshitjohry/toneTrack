

function bytesToBase64(bytes) {
  const binString = String.fromCodePoint(...bytes);
  return btoa(binString);
}

const url = 'http://34.132.128.184/';
const chunk_size = 20;
slice = 0;
audioChunks = [];
const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    

    mediaRecorder.addEventListener("dataavailable", event => {
      console.log("New event!!!");
      audioChunks.push(event.data);
      const audioBlob = new Blob(audioChunks, {type: 'audio/wav'});
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      
      reader.onloadend = () => {
        base64data = reader.result.split(',')[1];
        // slice = chunk_size*(audioChunks.length-1);
        // slice += chunk_size;
        user = document.getElementById("uname").value + "_" + slice;
        const ans = JSON.stringify({mp3: base64data, filename: user})
        console.log(user);
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
          slice += chunk_size;
          audioChunks=[];
          startRecording();
        });
  
      }
      
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
