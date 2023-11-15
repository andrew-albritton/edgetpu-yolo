
import os
import pandas as pd
import time
from periphery import SPI
from periphery import GPIO
import time
import os

'''
this file will be used to take in images from our camera
- then process them to size 640x640
- then send photos through detection using os command
- then pull detected objects from output csv from above line and perform following steps
- average out detection accross the three species of interest
- whichever species has the highest average will then be sent to the GPI/O pins for transmitter application


***input***
images for detection


***output*** 
final descision label for transmission 
'''




# Getting file_names_array using this function
def get_file_names(folder_path):
    try:
        # Get a list of files in the specified folder
        file_names = os.listdir(folder_path)

        # Filter out subdirectories and keep only file names
        file_names = [file for file in file_names if os.path.isfile(os.path.join(folder_path, file))]

        return file_names
    
    except OSError as e:
        print(f"An error occurred: {e}")
        return []


###
'''
insert code here to use above functions for image processing
'''

# GPIO pin initialization
motionsensor = GPIO("/dev/gpiochip4", 13, "in")  # pin 36

try:
    while True:
        try:
            state = motionsensor.read()
            print("waiting for motion")

            if state:
                print("Motion Detected! Running Classification...")
                os.system("python3 detect.py -m final_weights-int8_edgetpu.tflite --names data.yaml --conf_thresh 0.5 --stream --device 1")
                time.sleep(3.0)
    
                #grabbing data from csv
                dataframe = pd.read_csv("detections.csv", header=None)   
                length = dataframe.shape[0]
                found_labels = dataframe.loc[0:length, 0]
                found_probs = dataframe.iloc[0:length, 1]
                found_probs = found_probs.to_numpy()
                flycount = 0.
                flyprob = 0.
                lizardcount = 0.
                lizardprob = 0.
                rodentcount = 0.
                rodentprob = 0.
                foundfly = False
                foundliz = False
                foundrat = False
                ratscore = 0.
                flyscore = 0.
                lizardscore = 0.
                #counts of each category requireing frequency emission
                #possible labels - names: ['0', 'Dogs', 'Fruitfly', 'Human Body', 'Lizards', 'Squirrel', 'aphid', 'fly', 'kid', 'person', 'rat']
                
                for i in range(0, len(found_labels) - 1):
                    condition = found_labels.iloc[i]
                    condition = str(condition)
                    if (condition == 'Fruitfly' or condition == 'fly' or condition == 'aphid'):
                        flycount += 1
                        flyprob += found_probs[i]
                        foundfly = True
                        
                    elif (condition == ('Lizards' or '0')):
                        lizardcount += 1
                        lizardprob += found_probs[i]
                        foundliz = True
                    
                    elif (condition == ('Squirrel' or 'rat')):
                        rodentcount += 1
                        rodentprob += found_probs[i]    
                        foundrat = True    
                
                #averaging scores
                if (foundrat == True):
                    ratscore = rodentprob / rodentcount
                if (foundfly == True):
                    flyscore = flyprob / flycount
                if (foundliz == True):
                    lizardscore = lizardprob / lizardcount
                
                scorelist = {'rat':ratscore, 'lizard':lizardscore, 'fly':flyscore}
                
                descision = max(scorelist, key=scorelist.get)
                
                print("rat averaged    prob: ", ratscore,'\n')
                print("lizard averaged prob: ", lizardscore, '\n')
                print("fly averaged    prob: ", flyscore, '\n')
                print("Transmit Frequency: "+descision)
                
                                
            f = open("detections.csv", "w+") #clearing saved data on detections.csv
            f.close()
                
            time.sleep(10)
        except Exception as e:
            print(f"An error occurred: {e}")
        
except KeyboardInterrupt:
    # Close GPIO when the program is interrupted
    motionsensor.close()
