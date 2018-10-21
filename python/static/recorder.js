console.log("this is a log");
navigator.mediaDevices.getUserMedia({audio:true})
	.then(stream => {
		rec = new MediaRecorder(stream);
		rec.ondataavailable = e => {
			audioChunks.push(e.data);
			if (rec.state == "inactive"){
        let blob = new Blob(audioChunks,{type:'audio/x-mpeg-3'});
        console.log("WE REACHED HERE LMAO");
        console.log(blob);
        $.ajax({
    url: 'http://localhost:8080/api/query',
    type: 'POST',
    data: [{'audioRaw': blob}],
    dataType: 'application/json',
    contentType: "application/json",
    complete: function(data){
        var responseList = data['responses'];
        console.log(data);
        for (var i = 0 ; i < responseList.length; i++){
            var nextResponse = responseList[i];
            console.log('response = ' + nextResponse);
        }
    },
    success: function(data){
        alert(data)
    }
});
        recordedAudio.src = URL.createObjectURL(blob);
        recordedAudio.controls=true;
        recordedAudio.autoplay=true;
        audioDownload.href = recordedAudio.src;
        audioDownload.download = 'audio.mp3';
        audioDownload.innerHTML = 'download';
     }
		}
	})
	.catch(e=>console.log(e));

var startRecord = document.getElementById("startRecord");
startRecord.onclick = e => {
  startRecord.disabled = true;
  stopRecord.disabled=false;
  audioChunks = [];
  rec.start();
}

var stopRecord = document.getElementById("stopRecord");
stopRecord.onclick = e => {
  startRecord.disabled = false;
  stopRecord.disabled=true;
  rec.stop();
}
