'use strict'

let log = console.log.bind(console),
    id = val => document.getElementById(val),
    ul = id('ul'),
    // gUMbtn = id('gUMbtn'),
    start = id('start'),
    stop = id('stop'),
    stream,
    recorder,
    counter = 1,
    chunks,
    media;

// const cors = require('cors');
// app.use(cors());
let mv = id('mediaVideo'),
    mediaOptions = {
        video: {
            tag: 'video',
            type: 'video/webm',
            ext: '.mp4',
            gUM: { video: true, audio: true }
        },
        audio: {
            tag: 'audio',
            type: 'audio/mpeg-3',
            ext: '.mp3',
            gUM: { audio: true }
        }
    };
media = mediaOptions.audio;
navigator.mediaDevices.getUserMedia(media.gUM).then(_stream => {
    stream = _stream;
    // id('gUMArea').style.display = 'none';
    id('btns').style.display = 'inherit';
    start.removeAttribute('disabled');
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => {
        chunks.push(e.data);
        if (recorder.state == 'inactive') makeLink();
    };
    log('got media successfully');
}).catch(log);

// gUMbtn.onclick = e => {

// }

start.onclick = e => {

    start.disabled = true;
    stop.removeAttribute('disabled');
    chunks = [];
    recorder.start();
}


stop.onclick = e => {
    stop.disabled = true;
    recorder.stop();
    // chunks = [];
    start.removeAttribute('disabled');
    let blob = new Blob(chunks, {type: "audio/mpeg-3"});
    sendData(blob);
    // fetch("http://localhost:5000/api/audio", { method: 'POST', body: fd })
};

function sendData(data) {
    var form = new FormData();
    form.append('file', data, 'data.mp3');
    form.append('title', 'data.mp3');
    //Chrome inspector shows that the post data includes a file and a title.
    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/api/audio',
        data: form,
        cache: false,
        processData: false,
        contentType: false
    }).done(function(data) {
        console.log(data);
    });
}

function makeLink() {
    let blob = new Blob(chunks, { type: media.type })
        , url = URL.createObjectURL(blob)
        , li = document.createElement('li')
        , mt = document.createElement(media.tag)
        , hf = document.createElement('a')
        ;
    mt.controls = true;
    mt.src = url;
    hf.href = url;
    hf.download = `${counter++}${media.ext}`;
    hf.innerHTML = `donwload ${hf.download}`;
    li.appendChild(mt);
    li.appendChild(hf);
    ul.appendChild(li);
}
