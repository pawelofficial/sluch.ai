
import dotenv 
import json 
dotenv.load_dotenv()

import openai
import os 
from sluchai.utils import setup_logger,purge_dir,CONFIG,create_dir

# Set your OpenAI API key
API_KEY = os.getenv("OPENAI_API_KEY")

# Path to your audio file




this_dir=os.path.dirname(os.path.abspath(__file__))
logs_path=os.path.join(this_dir,"logs")
LOGGER=setup_logger("windows_record",fp=os.path.join(logs_path,'stt.log') )



def stt(filename,user_dirs,client=None, lang=CONFIG['LANGUAGE'] ):

    input_dir=user_dirs['03_audio_slices']
    output_dir=user_dirs['04_stt_slices']
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


def stt_many(user_dirs):
    client = openai.OpenAI(api_key=API_KEY)

    files=os.listdir(user_dirs['03_audio_slices'])
    for file in files:
        stt(file,client=client,user_dirs=user_dirs)
        
        
def process_text_files(filename,user_dirs):
            
    input_dir=user_dirs['04_stt_slices']
    purge_dir(user_dirs['05_notes'],inclusive=False)
    output_dir=user_dirs['05_notes']
    output_dir2=user_dirs['07_user_notes']


    client = openai.Client()

    files=[os.path.join(input_dir,i)  for i in  os.listdir(input_dir)]
    filenames=os.listdir(input_dir)
    fulltext={}
    for no,file in enumerate(files):
        LOGGER.info(f"Processing {file}")
        with open(file, "r",encoding="utf-8") as f:
            text = f.read()
        ai_output=openai_completion(text,client=client)

        fulltext[filenames[no]]=ai_output
        
        with open(os.path.join(output_dir,filenames[no]),'w',encoding='utf-8') as f:
            f.write(ai_output)
        
    fulltext_filename=filename.replace('.wav','.txt')
    with open(os.path.join(output_dir2,fulltext_filename),'w',encoding='utf-8') as f:
        f.write('-------------------------------------------------------')
        for key,value in fulltext.items():
            f.write(f"{key}:\n")
            f.write(f"{value}\n")
            f.write("\n\n")
            f.write('-------------------------------------------------------')
        
    with open(os.path.join(user_dirs['permanent_user_dir'],fulltext_filename),'w',encoding='utf-8') as f:
        f.write('-------------------------------------------------------')
        for key,value in fulltext.items():
            f.write(f"{key}:\n")
            f.write(f"{value}\n")
            f.write("\n\n")
            f.write('-------------------------------------------------------')

    #json.dump(fulltext,open(os.path.join(output_dir2,'fulltext.json'),'w',encoding='utf-8'),indent=4 ,ensure_ascii=False)

        

        
        
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
            