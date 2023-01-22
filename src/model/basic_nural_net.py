import pickle
import numpy as np
import tensorflow as tf

# Load the data from the pickle file
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

# Convert the data to a NumPy array 
data = np.array(data)

# every row is a config
# every column is a value
# the last column is the output
# the first 3 columns are the input


# Split the data into input and output
x_train = data[:, :-1]
y_train = data[:, -1]
print(x_train.shape)


# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(x_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=10)

# Save the model
model.save('model.h5')
