// JS code for Speech to text
var SpeechRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition
    || window.mozSpeechRecognition || window.msSpeechRecognition)();

    const the_button = document.getElementById("the_button");
    the_button.addEventListener('click', function(event) {
        SpeechRecognition.start();
    })

    SpeechRecognition.onresult = function(event){
        var the_text = event.results[0][0].transcript;
        document.getElementById('the_form').value = the_text;
    };

    SpeechRecognition.onend = function(){
        SpeechRecognition.stop();
    };


function reloadPage() {
    location.reload();
}