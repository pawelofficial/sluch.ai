import sluchai


device=sluchai.windows_record.find_device()
#print(device)
#sluchai.windows_record.check_devices(device_index=device)
#sluchai.windows_record.start_recording(device_index=device)
#sluchai.windows_record.slice_file(filename='input.wav')
#sluchai.stt.stt('001_slice_0_35.wav')
#exit(1)
#sluchai.stt.stt_many()

prompt="""
Czarne dziury to jedne z najbardziej fascynujących obiektów we Wszechświecie. Są to regiony czasoprzestrzeni o tak silnej grawitacji, że nic – nawet światło – nie może ich opuścić. Granica czarnej dziury, zwana horyzontem zdarzeń, wyznacza punkt bez powrotu dla materii i promieniowania.

Zgodnie z ogólną teorią względności Einsteina, czarne dziury powstają, gdy ogromna masa zostaje skupiona w bardzo małej objętości, prowadząc do zakrzywienia czasoprzestrzeni w sposób uniemożliwiający ucieczkę jakiejkolwiek cząstki. Wyróżniamy kilka rodzajów czarnych dziur:

Czarne dziury gwiazdowe – powstają w wyniku kolapsu grawitacyjnego masywnych gwiazd.
Supermasywne czarne dziury – znajdują się w centrach galaktyk i mogą osiągać miliardy mas Słońca.
Pierwotne czarne dziury – hipotetyczne obiekty, które mogły powstać tuż po Wielkim Wybuchu.
Jednym z najważniejszych aspektów badania czarnych dziur jest ich wpływ na otoczenie. Chociaż same są niewidoczne, ich obecność zdradzają zjawiska takie jak dyski akrecyjne – gorąca materia opadająca na czarną dziurę – czy emisja promieniowania rentgenowskiego.

Paradoks informacyjny czarnych dziur, związany z teorią Hawkinga, sugeruje, że czarne dziury mogą powoli parować poprzez emisję promieniowania Hawkinga. To prowadzi do fundamentalnych pytań o naturę informacji i mechaniki kwantowej.

Badania nad czarnymi dziurami łączą ogólną teorię względności i fizykę kwantową, co czyni je kluczowym elementem poszukiwań jednolitej teorii grawitacji kwantowej. Dzięki projektom takim jak Event Horizon Telescope udało się nawet uchwycić cień czarnej dziury, co stanowi przełom w astrofizyce.
"""

#a=sluchai.stt.openai_completion(prompt=prompt)
sluchai.stt.process_text_files()