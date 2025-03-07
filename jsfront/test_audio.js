import fs from 'fs';
import fetch from 'node-fetch';
import FormData from 'form-data';

(async () => {
  const formData = new FormData();
  formData.append('file', fs.createReadStream('sample.wav'));

  const response = await fetch('http://127.0.0.1:8000/audio', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  console.log(result);
})();
