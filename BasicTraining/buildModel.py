from statistics import mode
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
import random

#load datasets
x = np.loadtxt("train_x3t.csv",delimiter=',')
y = np.loadtxt("train_y3t.csv",delimiter=',')
test_x = np.loadtxt("test_x3t.csv",delimiter=',')
test_y = np.loadtxt("test_y3t.csv",delimiter=',')
#build model
model = keras.Sequential([
    keras.layers.Dense(540, activation='relu', input_shape=[len(x[0])]),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(len(y[0]))
  ])
optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss=tf.keras.losses.Hinge(),
                optimizer=optimizer,
                metrics=['mae', 'mse'])
model.summary()

#train and from time to time ask user if the termination time did not come up
train = "Y"
epochList = []
maeList = []
while train[0].upper()=="Y":
    print("Training starts")
    EPOCHS = 140
    #early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    history = model.fit(x, y, batch_size=100,
                        epochs=EPOCHS, validation_data=(test_x,test_y), verbose=1, 
                        )
    #callbacks=[early_stop]
    #plot progress
    mae = history.history["mae"]
    maeList+=list(mae)
    epochList += list(range(len(epochList)+1,len(epochList)+len(mae) + 1))
    plt.plot(epochList, mae)
    plt.show()
    train = input("Should I perform a train cycle?(Y-yes/N-no):")
model.save("modelSelect3.h5")

#log some predictions
indxMax = len(test_x)
for i in range(60):
    indx = random.randint(0,indxMax-1)
    print("Predicted:",model.predict(test_x[indx][None]))
    print("Should be:",test_y[indx])