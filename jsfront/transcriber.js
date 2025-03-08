
const TRresponseDiv = document.getElementById('TRresponseDiv');

let processedTexts = new Set();

setInterval(() => {
    const texts = STTresponseDiv.querySelectorAll('p');

    texts.forEach(p => {
        const content = p.textContent;

        if (!processedTexts.has(content)) {
            processedTexts.add(content);

            fetch('http://127.0.0.1:8000/transcribe', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text: content })
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