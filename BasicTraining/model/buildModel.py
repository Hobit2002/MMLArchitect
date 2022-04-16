from gc import callbacks
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np

#load datasets
x = np.loadtxt("train_x.csv",delimiter=',')
y = np.loadtxt("train_y.csv",delimiter=',')
test_x = np.loadtxt("test_x.csv",delimiter=',')
test_y = np.loadtxt("test_y.csv",delimiter=',')
#build model

model = keras.Sequential([
    keras.layers.Dense(240, activation='relu', input_shape=[len(x[0])]),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
  ])
optimizer = keras.optimizers.Adam(learning_rate=0.00001)
model.compile(loss=tf.keras.losses.Hinge(),
                optimizer=optimizer,
                metrics=['mae', 'mse','accuracy'])
model.summary()

EPOCHS = 250
#early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
history = model.fit(x, y, batch_size=100,
                    epochs=EPOCHS, validation_data=(test_x,test_y), verbose=1, callbacks=[callback]
                    )
#callbacks=[early_stop]
#plot progress
epochList = []
maeList = []    
mae = history.history["mae"]
maeList+=list(mae)
epochList += list(range(len(epochList)+1,len(epochList)+len(mae) + 1))
plt.plot(epochList, mae)
plt.show()

model.save("model.h5")