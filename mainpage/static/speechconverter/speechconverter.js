click_to_convert.addEventListener('click', function(){
    var speech = true;
    window.SpeechRecognition = window.webkitSpeechRecognition;
    const sr = new SpeechRecognition();
    sr.interimResults = true;

    sr.addEventListener('result', e=>{
        const transcription = Array.from(e.results)
        .map(result =>result[0])
        .map(result => result.transcription)

        convert_text.innerHTML = transcription;
    })

    if(speech == true){
        sr.start();
    }
})