const recordBtn = document.getElementById('recordBtn');
const micIcon = document.getElementById('micIcon');
let mediaRecorder;
let audioChunks = [];
let interval;

recordBtn.onclick = async () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        clearInterval(interval);
        micIcon.src = 'mic-black.png';
    } else {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => audioChunks.push(event.data);

        mediaRecorder.onstop = () => {
            const blob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('file', blob, `audio_${Date.now()}.wav`);

            fetch('http://127.0.0.1:8000/audio', {
                method: 'POST',
                body: formData
            }).then(response => {
                if (!response.ok) {
                    console.error('Upload failed');
                }
            }).catch(err => console.error(err));

            audioChunks = [];
        };

        mediaRecorder.start();
        micIcon.src = 'mic-red.png';

        interval = setInterval(() => {
            mediaRecorder.stop();
            mediaRecorder.start();
        }, 5000);
    }
};
