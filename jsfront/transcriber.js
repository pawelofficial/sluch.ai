
const TRresponseDiv = document.getElementById('TRresponseDiv');
const usernameInput = document.getElementById('username');


let processedTexts = new Set();

setInterval(() => {
    const username = usernameInput.value;
    console.log(username);  // logs every 3 seconds
    console.log(window.isRecording);  // logs every 3 seconds

    
    if (!window.isRecording) return;  // stop if not recording
    const texts = STTresponseDiv.querySelectorAll('p');

    texts.forEach(p => {
        const content = p.textContent;

        if (!processedTexts.has(content)) {
            processedTexts.add(content);

            fetch('http://127.0.0.1:8000/transcribe', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text: username + content })
            })
            .then(res => res.json())
            .then(transcribed => {
                const newTranscription = document.createElement('p');
                newTranscription.textContent = transcribed.text || 'No transcription returned';
                newTranscription.style.margin = '5px 0';
                TRresponseDiv.appendChild(newTranscription);
                TRresponseDiv.scrollTop = TRresponseDiv.scrollHeight;
            })
            .catch(err => console.error(err));
        }
    });

}, 1000); // Checks every 1 second