  // New instance
  const recorder = new MicRecorder({
    bitRate: 128
  });

  console.log("binded");
  var button;

  window.addEventListener('DOMContentLoaded', function() {
    button = document.getElementById("recordButton");
    button.addEventListener('click', startRecording);
  });

  function startRecording() {
    recorder.start().then(() => {
      button.textContent = 'Stop recording';
      button.classList.toggle('btn-danger');
      button.removeEventListener('click', startRecording);
      button.addEventListener('click', stopRecording);
      console.log("starting recording");
    }).catch((e) => {
      console.error(e);
    });
  }

  function saveRecording(file) {
    // save to a specific local folder
  }

  function sendRecording(buffer) {
    $.ajax({
    type: 'GET',
    url: '/api/query',
    data: {'file': buffer},
    dataType: 'jsonp',
    success: function(jsonData) {
      var response_string = jsonData['response'];

      alert(jsonData);
    },
    error: function() {
      alert('Error loading ');
    }
  });
  }

  function stopRecording() {
    recorder.stop().getMp3().then(([buffer, blob]) => {
      const file = new File(buffer, 'music.mp3', {
        type: blob.type,
        lastModified: Date.now()
      });
      //sendRecording(file);

      //remove playback
      const li = document.createElement('li');
      const player = new Audio(URL.createObjectURL(file));
      player.controls = true;
      li.appendChild(player);
      document.querySelector('#playlist').appendChild(li);

      // keep this
      button.textContent = 'Start recording';
      button.classList.toggle('btn-danger');
      button.removeEventListener('click', stopRecording);
      button.addEventListener('click', startRecording);
      console.log("done recording");
    }).catch((e) => {
      console.error(e);
    });
  }
