import re
import time
import os
import cv2
import random
from shutil import copyfile, copy
from os.path import isfile, join, exists, isdir


#------------- PROGRESS BAR --------------#
# def: creates a progress bar to show preogressions of loops
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        print()

#--------- FILE STRUCTURE CREATION ----------#
# checks for required file structure and creates it if not found
def checkFileStruct ():
    curPath = os.getcwd()
    if exists(curPath + '/IMG_LIB'):
        print('IMG_LIB already exists')
    else:
        os.mkdir(curPath + '/IMG_LIB')

    if exists(curPath + '/IMG_PROC'):
        print('IMG_PROC already exists')
    else:
        os.mkdir(curPath + '/IMG_PROC')
        os.chdir(curPath + '/IMG_PROC')
        print("after change: ", os.getcwd())
        os.mkdir(os.getcwd() + '/Final Image Sequence')
        os.mkdir(os.getcwd() + '/EXPORT')

        os.chdir(curPath)

#------------- GRAIN GENERATOR --------------#
#generates the integer value of each grain and stores it in an array
def grain_generator(target_frame_total, avg_frame_len):

    grain_array = []
    frame_remaining = target_frame_total
    grain_end_frame = avg_frame_len + round(avg_frame_len * random.random())
    while frame_remaining != 0:

        sign = random.choice([-1,1])

        frame_remaining = frame_remaining - grain_end_frame
        grain_array.append(grain_end_frame)

        grain_end_frame = avg_frame_len + round(((avg_frame_len) * random.random() * sign))
        while grain_end_frame == 0:
            grain_end_frame = avg_frame_len + round(((avg_frame_len) * random.random() * sign))
            
        if grain_end_frame > frame_remaining:
            grain_end_frame = frame_remaining

    #print(sum(grain_array))
    #print(grain_array)
    return grain_array


#-------------------- SAMPLER ---------------------#    
#Grain Sampler Function will open an image library and query multiple folders for image sequences, 
#compile the results, and export an openCV image sequence

def sampler(grain_array, total_frames):

    #Grain characteristics: start frame, end frame, duration (total grain length in number of frames) 


    #Grabs IMG_LIB
    filePath = os.getcwd() + '/IMG_LIB/'  
    outPath = os.getcwd() +  '/IMG_PROC/Final Image Sequence/'


    # Delete existing files in Final_Image_Set
    temp_path = outPath
    files_del =[f for f in os.listdir(temp_path)if isfile(join(temp_path,f))]
    
    for q in range (len(files_del)):
        if os.path.exists(temp_path):
            os.remove(temp_path + '/' + files_del[q])
        else:
            print("The file does not exist")




    #gets list of directories in /IMG_LIB/
    imageDirs =[d for d in os.listdir(filePath) if isdir(join(filePath,d))]
    
    l = len(grain_array) #used for progress bar

    j = 1 #counter for renaming image files in ascending numeric order 

    printProgressBar(0, l, prefix = 'Sequencing:', suffix = 'Complete', length = 50)
    for n in range(0,len(grain_array)):
    #--loop determines start and end frame as well as copying the files    
        printProgressBar(n+1, l, prefix = 'Sequencing:', suffix = 'Complete', length = 50)

        randDir= filePath + imageDirs[random.randint(0, len(imageDirs)-1)]      #picks random directory within /IMG_LIB/
        images = sorted(os.listdir(randDir))   #pulls all images from randDir and stores them
        while ((len(images)-grain_array[n]) <= 0) :
            randDir= filePath + imageDirs[random.randint(0, len(imageDirs)-1)] 
            images = sorted(os.listdir(randDir))
        

        
        



        start_frame = random.randrange(1,len(images)-grain_array[n])  #picks a random start frame

        end_frame = start_frame + grain_array[n]                                #calculates end frame from int stored in grain_array[]

        ###--Re_rolls if end frame is bed bath and beyond
        while end_frame >= len(images): 
            start_frame = random.randrange(1,len(images)-grain_array[n])
            end_frame = start_frame + grain_array[n]


        ##--actual copying occurs-----
        
        for i in range(start_frame, end_frame) :

            copy(randDir + "/"+ images[i], outPath + str(j) + ".jpg")
            j=j+1



    #The resulting image files will be accesible in the /IMG_PROC/Final Image Sequence/ folder 
    return outPath


#---------------- VIDEO CONVERTER -----------------#
# This function converts the single images in the Final_Image_Set folder into an image sequence using openCV functionality

def convert(pathIn2, pathOut2, fps, time, dim):
    frame_array = []
    files = []
    #---sorts files into correct order---#
    l = len(os.listdir(pathIn2))
    i=1
    while i <= l:
        files.append(str(i) + '.jpg')
        i = i+1
    #------------------------------------#

    if l == 0:
        print("No Files in folder!")
        exit()
    print("Number of files in path: ", len(files))
    printProgressBar(0, l, prefix = 'Resizing:', suffix = 'Complete', length = 50)
    for i in range (len(files)):
       
       try :
            printProgressBar(i+1, l, prefix = 'Resizing:', suffix = 'Complete', length = 50)
            filename=pathIn2 +files[i]
            img=(cv2.imread(filename))
            img=cv2.resize(img, dim)
            height, width, layers = img.shape
            size =(width,height)
            frame_array.append(img)
       except Exception as e:
            print(e)
            print("----VIDEO COMPILE ERROR----")

    out=cv2.VideoWriter(pathOut2, cv2.VideoWriter_fourcc(*"mp4v"),fps, size)
    printProgressBar(0, l, prefix = 'Creating Video:', suffix = 'Complete', length = 50)

    for i in range(len(frame_array)):
        printProgressBar(i+1, l, prefix = 'Creating Video:', suffix = 'Complete', length = 50)
        out.write(frame_array[i])
        
    

    out.release()

#------------ MAIN --------------#

ext = '.mp4'                                                                #video type, DO NOT CHANGE
target_frame_sec = int(input("Enter target video total time in seconds: ")) #target video length in seconds
fps = int(input("Enter target video frames per second: "))                  #frames per second
target_frame_total = target_frame_sec * fps                                 #total number of frames
print("Target Frame Total: ", target_frame_total)


#x = int(input("Enter target video horizontal resolution: "))
#y = int(input("Enter target video vertical resolution: "))
dim = 1200,800 #(x, y)

checkFileStruct() #checks for the required file structure

#--------name video file and check for existing-------#
videoFileName = input("Enter name for video file:")
videoPath = '/IMG_PROC/EXPORT/' + videoFileName + ext

id = 1
while isfile(os.getcwd() + videoPath):
    videoFileName = videoFileName + str(id)
    videoPath = '/IMG_PROC/EXPORT/' + videoFileName + ext
    id = id+1
#------------------------------------------------------#


avg_frame_len = int(input("Enter target average grain frame length: "))
x = grain_generator(target_frame_total, avg_frame_len) # Generate grains required to hit target_frame_total
pathIn2 = sampler(x, target_frame_total)   
pathOut2 = os.getcwd() + videoPath
print("video's destination: ", pathOut2)
time=1 #changes the number of times the image is looped 

convert(pathIn2,pathOut2,fps,time, dim)
print('Completed!')






