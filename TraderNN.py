import tensorflow as tf
import numpy as np
import os
from math import ceil

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

data = open("sp500.csv", "r")

X = np.zeros((921300, 10, 2), dtype=np.float32)
Y = np.zeros((921300), dtype=np.float32)

def loadXY():
    global X
    global Y

    Raw = np.zeros((1950, 16380), dtype=np.float32)

    for x in range(3): data.readline()
    for x in range(1950):
        line = data.readline().split(",")
        line.pop(0)
        for y in range(2500):
            if line[y] == "":
                Raw[x][y] = 0
            else:
                Raw[x][y] = float(line[y])

    np.save("Raw.npy", Raw)

    for day in range(5):
        for trial in range(370):
            for company in range(498):
                for x in range(10):
                    if Raw[day * 390 + trial + x + 1][company * 5] == 0 or Raw[day * 390 + trial + x][company * 5] == 0:
                        X[day * 184260 + trial * 498 + company][x][0] = 0
                        X[day * 184260 + trial * 498 + company][x][1] = 0
                    else:
                        X[day * 184260 + trial * 498 + company][x][0] = (Raw[day * 390 + trial + x + 1][company * 5] - Raw[day * 390 + trial + x][company * 5]) / Raw[day * 390 + trial + x][company * 5]
                        X[day * 184260 + trial * 498 + company][x][1] = Raw[day * 390 + trial + x][company * 5 + 4] / 1000000
                for y in range(10):
                    try:
                        if (Raw[day * 390 + trial + 9 + y][company * 5 + 3] - Raw[day * 390 + trial + 9][company * 5 + 3]) / Raw[day * 390 + trial + 9][company * 5 + 3] > 0.005:
                            Y[day * 184260 + trial * 498 + company] = 1
                    except Exception as ex:
                        pass

#X = np.load("X.npy")
#Y = np.load("Y.npy")

loadXY()

X_train = X[:800000]
Y_train = Y[:800000]

X_test = X[800000:]
Y_test = Y[800000:]

np.save("X.npy", X)
np.save("Y.npy", Y)

checkpoint_path = "v5/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(10, 2)),
    tf.keras.layers.Dense(2048, activation='tanh'),
    tf.keras.layers.Dense(4096, activation='linear'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(8192, activation='tanh'),
    tf.keras.layers.Dense(8192, activation='linear'),
    tf.keras.layers.Dense(8192, activation='tanh'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(4096, activation='linear'),
    tf.keras.layers.Dense(2048, activation='tanh'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

loss_fn = tf.keras.losses.MeanSquaredError()

model.compile(optimizer="adam", loss=loss_fn, metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=20, validation_data=(X_test, Y_test), callbacks=[cp_callback])
