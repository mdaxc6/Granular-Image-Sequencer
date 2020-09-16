# Granular-Image-Sequencer


***RIGHT NOW THE PROGRAM WILL FAIL ON THE FIRST RUNN***
1. The first time you run the script it will create two directories in the path that scrip is located.
    -The directories created will me IMG_LIB and IMG_PROC
2. After running the script and letting it fail, populate the IMG_LIB directory that was created with images.
    -the images must be inside a folder within IMG_LIB, but you can have as many folders as you like.
    -I recommend taking videos and converting them into their individual frames,
     and then put those frames into a directory within IMG_LIB. The idea is to have multiple directories full of images within IMG_LIB
     
3. After populating IMG_LIB with images, running the script again will propt you for:
  -Video length in seconds
  -Desired framerate
  -Video filename (mp4)
  -Average grain length (int)

4. The script will notify you of completion, and the resulting video file will be located in IMG_PROC/EXPORT with the filename you provided



NOTES:
When working with very large image sets, and longer videos, the script uses a LOT of RAM currently. We are working on a way to optimize it.

If you provide ranom images, instead of frames from a video, the result will be very random, which could also be desired.
    
    

