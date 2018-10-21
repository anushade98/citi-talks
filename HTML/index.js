function handleFileSelect(evt) {
var reader = new FileReader();

reader.onload = function(e) {
  document.getElementById("target").innerHTML = reader.result;
  var msg = new SpeechSynthesisUtterance(reader.result);
  window.speechSynthesis.speak(msg);
};

reader.readAsText(this.files[0]);
}

$(document).ready(function () {
$('#file').change(handleFileSelect);
});
