import pandas as pd
import os
import shutil
import random

esc50_csv_path = r"C:\Users\Scrap\OneDrive\Documents\Homework\CSCE585\CVDisasterRescue\sound_classification\data\ESC-50-master\ESC-50-master\meta\esc50.csv"
esc50_files_path = r"C:\Users\Scrap\OneDrive\Documents\Homework\CSCE585\CVDisasterRescue\sound_classification\data\ESC-50-master\ESC-50-master\audio\\"

output_dir = r"C:\Users\Scrap\OneDrive\Documents\Homework\CSCE585\CVDisasterRescue\sound_classification\data"
csv_data = pd.read_csv(esc50_csv_path)
#print(csv_data['category'].unique())

human_sounds =['clapping', 'footsteps', 'brushing_teeth', 'drinking_sipping',
               'laughing', 'breathing', 'crying_baby', 'coughing', 'snoring',
               'sneezing']

for index, row in csv_data.iterrows():
    filepath = os.path.join(esc50_files_path, row[0])
    if row[3] in human_sounds:
        shutil.copy(filepath, os.path.join(output_dir, "human_sounds", row[0]))
    else:
        shutil.copy(filepath, os.path.join(output_dir, "nonhuman_sounds", row[0]))
    

nonhuman_dir = os.path.join(output_dir, "nonhuman_sounds")
human_dir = os.path.join(output_dir, "human_sounds")

flickr_audio_wav_dir = "./flickr_audio/wavs"
flickr_files = os.listdir(flickr_audio_wav_dir)
random.shuffle(flickr_files)

nonhuman_filecount = len([file for file in os.listdir(nonhuman_dir) if os.path.isfile(os.path.join(nonhuman_dir, file))])
human_filecount = len([file for file in os.listdir(human_dir) if os.path.isfile(os.path.join(human_dir, file))])

if human_filecount < nonhuman_filecount:
    while human_filecount != nonhuman_filecount:
       added_file = flickr_files.pop(0)
       shutil.copy(os.path.join(flickr_audio_wav_dir, added_file), 
                   os.path.join(human_dir, added_file))
       human_filecount += 1