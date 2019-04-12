# Convolutional Neural Network

# Installing Theano
# pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

# Installing Tensorflow
# pip install tensorflow

# Installing Keras
# pip install --upgrade keras

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 5, activation = 'sigmoid'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)
#E:/DataScience/Projects/Keras_CNN_Classification/Cats_Dogs/PetImages
training_set = train_datagen.flow_from_directory('F:/GitHub/Projects/Keras_CNN_Classification/Person_Classification/Images',
                                                 target_size = (64, 64),
                                                 batch_size = 32
                                                 )

test_set = test_datagen.flow_from_directory('F:/GitHub/Projects/Keras_CNN_Classification/Person_Classification/Images',
                                            target_size = (64, 64),
                                            batch_size = 32
                                            )

classifier.fit_generator(training_set,
                         steps_per_epoch = 8000,
                         epochs = 1,
                         validation_data = test_set,
                         validation_steps = 2000)
"""
# serialize model to JSON
model_json = classifier.to_json()
with open("PersonClassification.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
classifier.save_weights("PersonClassification.h5")
print("Saved model to disk")
 
."""
 """
# load json and create model
json_file = open('PersonClassification.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("PersonClassification.h5")
print("Loaded model from disk")
 
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
"""
# Part 3 - Making new predictions

import numpy as np
from keras.preprocessing import image
import matplotlib.pyplot as plt 
test_image = image.load_img('E:/DataScience/Projects/Keras_CNN_Classification/Person_Classification/venkat.jpg', target_size = (64, 64))
plt.imshow(test_image)
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = loaded_model.predict(test_image)
print(training_set.class_indices)
if result[0][0] == 1:
    print("Hemanth")
elif result[0][1] == 1:
    print("Lokesh")
elif result[0][2] ==1:
    print("Ramesh")
elif result[0][3]==1:
    print("Srinivas")
elif result[0][4]==1:
    print("Venkat")
else:
    print("Alien")