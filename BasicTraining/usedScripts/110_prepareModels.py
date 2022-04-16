import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np
import random

#loop through mks offering multiple possibilities
root = "s:/git/MMLarchitect/"
for i in range(21,30):
    #load sets
    mkRoot = root + "modKeySets/mk%i/"
    x = np.loadtxt(mkRoot%(i) + "train_x.csv",delimiter=',')
    y = np.loadtxt(mkRoot%(i) + "train_y.csv",delimiter=',')
    test_x = np.loadtxt(mkRoot%(i) + "test_x.csv",delimiter=',')
    test_y = np.loadtxt(mkRoot%(i) + "test_y.csv",delimiter=',')
    #build model
    model = keras.Sequential([
    keras.layers.Dense(30, activation='relu', input_shape=[len(x[0])]),
    keras.layers.Dense(10, activation='relu'),
    keras.layers.Dense(len(y[0]))
  ])
    optimizer = keras.optimizers.Adam(learning_rate=0.000001)
    model.compile(loss=tf.keras.losses.Hinge(),
                    optimizer=optimizer,
                    metrics=['mae', 'mse'])
    model.summary()
    #train and from time to time ask user if the termination time did not come up
    train = "Y"
    epochList = []
    maeList = []
    EPOCHS = 55
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
    model.save(mkRoot + "model.h5"%(i))