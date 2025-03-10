const recordBtn = document.getElementById('recordBtn');
const micIcon = document.getElementById('micIcon');
const STTresponseDiv = document.getElementById('STTresponseDiv');


let mediaRecorder;

recordBtn.onclick = async () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        micIcon.src = 'mic-black.png';
        micIcon.classList.remove('recording');
        window.isRecording = false; // stopped
    } else {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            const formData = new FormData();
            formData.append('file', event.data, `audio_${Date.now()}.wav`);

            fetch('http://127.0.0.1:8000/audio', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const newText = document.createElement('p');
                newText.textContent = data.text || 'No text returned';
                STTresponseDiv.appendChild(newText);
                STTresponseDiv.scrollTop = STTresponseDiv.scrollHeight;
            })
            .catch(err => console.error(err));
        };

        mediaRecorder.start(5000);
        micIcon.src = 'mic-red.png';
        micIcon.classList.add('recording');
    }

    window.isRecording = mediaRecorder.state === 'recording';
};
