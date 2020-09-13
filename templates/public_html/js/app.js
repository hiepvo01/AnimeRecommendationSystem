//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
    console.log("recordButton clicked");
    var constraints = { audio: true, video: false }

    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        audioContext = new AudioContext();
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input, { numChannels: 1 })
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function pauseRecording() {
    console.log("pauseButton clicked rec.recording=", rec.recording);
    if (rec.recording) {
        //pause
        rec.stop();
        pauseButton.innerHTML = "Resume";
    } else {
        //resume
        rec.record()
        pauseButton.innerHTML = "Pause";
    }
}

function stopRecording() {
    console.log("stopButton clicked");

    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    //reset button just in case the recording is stopped while paused
    pauseButton.innerHTML = "Pause";

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
}
var i = 0

function createDownloadLink(blob) {
    const form = {
        project_id: 'animebot-cbaheo',
        session_id: 'a',
        language_code: 'en',
    };
    const response = {
        user_response: '',
        dialogflow_response: '',
    };
    if ("WebSocket" in window) {
        // Let us open a web socket
        var ws = new WebSocket("ws://127.0.0.1:8000/chat");
        alert("WebSocket is supported by your Browser!");
        ws.onmessage = function(evt) {
            console.log(i)
            var data = JSON.parse(evt.data);
            alert("Message is received...");
            console.log(data.user_response);
            console.log(data.dialogflow_response);
            var user_str = document.createElement('p');
            user_str.innerHTML = data.user_response.toString();
            var bot_str = document.createElement('p');
            bot_str.innerHTML = data.dialogflow_response.toString();

            var elem1 = document.createElement("img");
            elem1.setAttribute("src", "avatarhuman.png");
            var user = document.createElement("div");
            user.classList.add("container");
            user.appendChild(elem1);
            user.appendChild(user_str);
            var dt = new Date();
            var time = "time" + i.toString();
            fulltime = '<span id=' + '"' + time + '"' + ' class="time-right"></span>';
            console.log(fulltime);
            user.innerHTML += fulltime;
            document.getElementById("conversation").appendChild(user);
            document.getElementById(time).innerHTML = dt.toLocaleTimeString();

            i = i + 1;
            var time = "time" + i.toString();
            fulltime = '<span id=' + '"' + time + '"' + ' class="time-right"></span>';

            var elem2 = document.createElement("img");
            elem2.setAttribute("src", "avatar.png");
            var bot = document.createElement("div");
            bot.classList.add("container");
            bot.appendChild(elem2);
            bot.appendChild(bot_str);
            bot.innerHTML += fulltime;

            document.getElementById("conversation").appendChild(bot);
            document.getElementById(time).innerHTML = dt.toLocaleTimeString();

            i = i + 1;
            var time = "time" + i.toString();
            fulltime = '<span id=' + '"' + time + '"' + ' class="time-right"></span>';
        };

        ws.onclose = function() {

            // websocket is closed.
            alert("Connection is closed...");
        };
    } else {

        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
    }
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.addEventListener('loadend', () => {
        const audioBase64 = reader.result.toString();
        const audioTurned = audioBase64.substr(audioBase64.indexOf(',') + 1);
        audio64 = audioTurned;
        const list = [JSON.stringify(form.project_id), JSON.stringify(form.session_id), JSON.stringify(audio64), JSON.stringify(form.language_code)];
        ws.send(list.toString())
        alert("Message is sent...");
    });
}