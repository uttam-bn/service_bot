from PIL import Image
import numpy as np
from io import BytesIO
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Data preparation
data_dir = 'dataset'
img_height, img_width = 128, 128
batch_size = 32
epochs = 5

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,  
    horizontal_flip=True,
    vertical_flip=True,
    rotation_range=20,
    zoom_range=0.2,
    shear_range=0.2
)

train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)


base_model = MobileNetV2(input_shape=(img_height, img_width, 3),
                         include_top=False,
                         weights='imagenet')
base_model.trainable = False  

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(train_generator.num_classes, activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=epochs
)

# Save the class indices
class_indices = train_generator.class_indices

def verify_image(image, class_indices, img_height=128, img_width=128):
    
    img = Image.open(image)
    img = img.resize((img_height, img_width))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Predict the class of the image
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    accuracy = predictions[0][predicted_class[0]]
    class_labels = {v: k for k, v in class_indices.items()}
    
    
    folder_name = class_labels.get(predicted_class[0], None)
    
    
    leaf_keywords = ['leaf', 'leaves']
    if folder_name and any(keyword in folder_name.lower() for keyword in leaf_keywords):
        return "Leaf", 0.0
    else:
        return folder_name, accuracy

