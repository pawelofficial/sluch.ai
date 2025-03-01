import sluchai as sai
import os 
import datetime
import shutil 
this_dir=os.path.dirname(os.path.abspath(__file__))
data_dir=os.path.join(this_dir,"data")


# workflow 1 - expects user input in 01_user_input dir 
ts_now=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
##ts_now='20250301_195328'

# purge data 
sai.utils.purge_dir(data_dir,inclusive=False)

# make user dirs 
user_dirs=sai.utils.make_temp_data_dirs(name=ts_now) 
##user_dirs=sai.utils.get_user_dirs(name=ts_now)

# copy example file 
shutil.copy(os.path.join(this_dir,'sluchai','input.mp3'), user_dirs['01_user_input'])


# convert to wav 
sai.windows_record.mp3_to_wav('input.mp3',user_dirs=user_dirs)

# slice wav file
sai.windows_record.slice_file('input.wav',user_dirs=user_dirs)

# do stt 
sai.stt.stt_many(user_dirs)

# process text files
sai.stt.process_text_files(user_dirs)



###exit(1)
####sai.utils.purge_dir(data_dir,inclusive=False)
###
###
###
###
###
###
###device=sai.windows_record.find_device()
###sai.windows_record.check_devices(device_index=device)
####sai.windows_record.start_recording(device_index=device,user_dirs=user_dirs)
###
###
####sai.windows_record.slice_file(filename='input.wav',user_dirs=user_dirs)
###
####sai.stt.stt_many(user_dirs)
###sai.stt.process_text_files(user_dirs)
###
####sai.stt.stt('001_slice_0_35.wav')
####exit(1)
###
###
###prompt="""
###Czarne dziury to jedne z najbardziej fascynujących obiektów we Wszechświecie. Są to regiony czasoprzestrzeni o tak silnej grawitacji, że nic – nawet światło – nie może ich opuścić. Granica czarnej dziury, zwana horyzontem zdarzeń, wyznacza punkt bez powrotu dla materii i promieniowania.
###
###Zgodnie z ogólną teorią względności Einsteina, czarne dziury powstają, gdy ogromna masa zostaje skupiona w bardzo małej objętości, prowadząc do zakrzywienia czasoprzestrzeni w sposób uniemożliwiający ucieczkę jakiejkolwiek cząstki. Wyróżniamy kilka rodzajów czarnych dziur:
###
###Czarne dziury gwiazdowe – powstają w wyniku kolapsu grawitacyjnego masywnych gwiazd.
###Supermasywne czarne dziury – znajdują się w centrach galaktyk i mogą osiągać miliardy mas Słońca.
###Pierwotne czarne dziury – hipotetyczne obiekty, które mogły powstać tuż po Wielkim Wybuchu.
###Jednym z najważniejszych aspektów badania czarnych dziur jest ich wpływ na otoczenie. Chociaż same są niewidoczne, ich obecność zdradzają zjawiska takie jak dyski akrecyjne – gorąca materia opadająca na czarną dziurę – czy emisja promieniowania rentgenowskiego.
###
###Paradoks informacyjny czarnych dziur, związany z teorią Hawkinga, sugeruje, że czarne dziury mogą powoli parować poprzez emisję promieniowania Hawkinga. To prowadzi do fundamentalnych pytań o naturę informacji i mechaniki kwantowej.
###
###Badania nad czarnymi dziurami łączą ogólną teorię względności i fizykę kwantową, co czyni je kluczowym elementem poszukiwań jednolitej teorii grawitacji kwantowej. Dzięki projektom takim jak Event Horizon Telescope udało się nawet uchwycić cień czarnej dziury, co stanowi przełom w astrofizyce.
###"""
###
####a=sai.stt.openai_completion(prompt=prompt)
####sai.stt.process_text_files()
###
####sai.utils.make_temp_data_dirs()
####dic=sai.utils.get_user_dirs()
####print(dic)
####C:\gh\sluch.ai\data