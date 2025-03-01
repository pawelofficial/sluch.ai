
import dotenv 
import json 
dotenv.load_dotenv()

import openai
import os 
from sluchai.utils import setup_logger,purge_dir,CONFIG

# Set your OpenAI API key
API_KEY = os.getenv("OPENAI_API_KEY")

# Path to your audio file
audio_file_path = "path/to/your/file.wav"


def stt(filename,client=None, lang='pl',input_dir=None,output_dir=None):
    this_dir=os.path.dirname(os.path.abspath(__file__))
    if not input_dir:
        input_dir=os.path.join(this_dir,'slices')
    if not output_dir:
        output_dir=os.path.join(this_dir,'slices_transcripts')

    if not client:
        client = openai.Client()

    audio_file_path=os.path.join(input_dir,filename)
    print(audio_file_path)
    # Open the file in binary mode

    with open(audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pl"  # Specify Polish language
        )

    # Print the transcribed text
    print("Transcription:", response.text)
    transcript_fp=os.path.join(output_dir,filename.replace('.wav','.txt'))
    with open(transcript_fp,'w',encoding="utf-8") as f:
        f.write(response.text)


def stt_many(dirname='slices'):
    client = openai.OpenAI(api_key=API_KEY)
    this_dir=os.path.dirname(os.path.abspath(__file__))
    fp=os.path.join(this_dir,dirname)
    files=os.listdir(fp)
    for file in files:
        stt(file,client=client,input_dir=fp)
        
        
def process_text_files(dirname='slices_transcripts',output_dirname='processed_slices'):
    
    this_dir=os.path.dirname(os.path.abspath(__file__))
    output_fp=os.path.join(this_dir,output_dirname)
    purge_dir(output_fp)
    input_dir=os.path.join(this_dir,dirname)
    client = openai.Client()

    files=[os.path.join(input_dir,i)  for i in  os.listdir(input_dir)]
    filenames=os.listdir(input_dir)
    fulltext={}
    for no,file in enumerate(files):
        with open(file,'r',encoding='utf-8') as f:
            text=f.read()
        ai_output=openai_completion(text,client=client)

        fulltext[filenames[no]]=ai_output
        
        with open(os.path.join(output_fp,filenames[no]),'w',encoding='utf-8') as f:
            f.write(ai_output)

    json.dump(fulltext,open(os.path.join(output_fp,'fulltext.json'),'w',encoding='utf-8'),indent=4 )

        

        
        
def openai_completion(prompt
                      ,system_message=CONFIG['SYSTEM_MESSAGE'] 
                      , model="gpt-4-turbo"
                      , client = None 
                      , temperature=0.7
                      , max_tokens=None):
    print('calling openai')


    if not client:
        client = openai.Client()
    
    messages = [{"role": "system", "content": system_message}
                ,{"role": "user", "content": prompt}]
                
        
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception as e:
        print(e)
        return "error"
        
    return response.choices[0].message.content
            