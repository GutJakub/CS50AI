import cv2
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    if not os.path.exists(data_dir):
        raise TypeError("data dir is not a existing directory")
    labels=[]
    images=[]
    for label in range(NUM_CATEGORIES):
        directory=os.path.join(data_dir,str(label))
        for file in os.listdir(directory):
            img=os.path.join(directory,file)
            img=cv2.imread(cv2.samples.findFile(img))
            img=cv2.resize(img,(IMG_WIDTH,IMG_HEIGHT))
            images.append(img)
            labels.append(label)
            
    
    return (images,labels)



def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    
    data_augmentation = Sequential(
      [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
      ]
    )
    model1 = Sequential([
      #data_augmentation,
      layers.Rescaling(1./255, input_shape=(30, 30, 3)),
      layers.Conv2D(32, 3, padding='same', activation='relu'), #ilosc filtri ktory stworzy dla danej wartstwy i obrazu
      layers.MaxPooling2D(),
      #layers.Dropout(0.05),
      layers.Conv2D(64, 3, padding='same', activation='relu'),
      layers.MaxPooling2D(),
      #layers.Dropout(0.1),
      layers.Conv2D(128, 3, padding='same', activation='relu'),
      layers.MaxPooling2D(),
      #layers.Dropout(0.2),
      layers.Flatten(),
      
      layers.Dense(256, activation='relu'), #HIDDEN LAYER
      layers.Dropout(0.5),
      layers.Dense(NUM_CATEGORIES,activation='softmax') #OUTPUT nasze rodzaje kwiatkow i kategorycznee przypisanie softmax
    ])
    model1.compile(optimizer='adam',
                  #loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  loss='categorical_crossentropy',
                   #loss="binary_crossentropy",
                  metrics=['accuracy'])
    return model1
    
    #raise NotImplementedError


if __name__ == "__main__":
    main()
