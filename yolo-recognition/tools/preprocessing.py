import os, glob, random, shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt  
import matplotlib.image as mpimg
from PIL import Image
import skimage
from skimage import io


# dataset paths

root_data_dir = 'yolo-recognition/OIDv4_ToolKit/OID/data/Dataset'
# split into test, train, and validation datasets

class_names = ['Human_head', 'Human_leg', 'Human_hand', 'Human_foot', 'Human_body', 'Human_arm']
# classes the model is trained to recognize from a picture

dataset_types = ['test', 'train', 'validation']

def generate_random_file_path(): # used to pick a random image and test with
    try:
        root = f'data/Dataset/{random.choice(dataset_types)}/{random.choice(class_names)}/'
        suffix = random.choice([file for file in os.listdir(root) if file.endswith('.jpg')])
        return f'{root}{suffix}'
    except:
        generate_random_file_path()

def normalize(path):
    base_image = io.imread(path)
    base_image_pixels = np.asarray(base_image)
    base_image_pixels = base_image_pixels.astype('float32')
    base_image_pixels /= 255.0
    return base_image_pixels


def imageboard():
    ## testing operations
    test_img = generate_random_file_path()
    image = io.imread(test_img)

    # plot image for each color channel
    i, (i1, i2, i3, i4, i5, i6) = plt.subplots(1, 6, sharey=True)
    i.set_figwidth(20)
    i.suptitle(test_img)

    i1.imshow(image)  #Original image
    i1.set_title('Original image')

    i2.imshow(image[:, : , 0]) #Red
    i2.set_title('Red channel')

    i3.imshow(image[:, : , 1]) #Green
    i3.set_title('Green channel')

    i4.imshow(image[:, : , 2]) #Blue
    i4.set_title('Blue channel')

    i5.imshow(skimage.color.rgb2gray(image), cmap='gray')
    i5.set_title('Grayscale')

    i6.imshow(normalize(test_img))
    i6.set_title('Normalized')

    plt.show()


# Note, YOLO resizes images automatically. 

def preprocess(dataset_type): # dataset_type being train, test, validation
    for i in range(0, len(class_names)): # number of training classes
        current_image_directory = f'data/Dataset/{dataset_type}/{class_names[i]}'
        for image in Path(current_image_directory).glob('*.jpg'):
            # if (io.imread(image).ndim != 3): # image is in full color as it has 3 dimensions in its image array
            io.imsave(image, normalize(image)) # overwrites image with it's normalized version!

# preprocess('train')
imageboard()