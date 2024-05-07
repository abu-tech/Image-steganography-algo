import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import numpy as np 
import cv2 

def mean_squared_error(original, Stego): 
    # the 'Mean Squared Error' between the two images is the 
    # # sum of the squared difference between the two images; 
    # # NOTE: the two images must have the same dimension 
    err = np.sum((original.astype("float") - Stego.astype("float")) ** 2) 
    err /= float(original.shape[0] * original.shape[1])


    # return the MSE, the lower the error, the more "similar" 
    # the two images are 
    return err 


def compare_images(Original_Image,Stego_Image,title):  
    #calculating MSE    
    mse = mean_squared_error(Original_Image,Stego_Image)    
    print("mse is " + str(mse))    
    #show the figure    
    fig = plt.figure(title)    
    plt.suptitle("Mean Squared Error: %.10f" %(mse))    
    
    #show the first image    
    ax = fig.add_subplot(1,2,1)    
    plt.imshow(Original_Image)    
    ax.title.set_text('Original Image')    
    plt.axis("off")    
    
    #show the second image    
    ax = fig.add_subplot(1,2,2)    
    plt.imshow(Stego_Image)    
    ax.title.set_text('Stego Image')    
    plt.axis("off")    
    plt.show() 
    
#loading the images 
original = mpimg.imread("y.jpg") 
stego = mpimg.imread("out_y.jpg") 
    
#calling the function 
compare_images(original,stego,"IMAGE STEGANOGRAPHY")
 