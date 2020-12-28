import numpy as np

data = open("data_an.csv", "r")

X = np.zeros((6060600, 10, 2), dtype=np.float32)
Y = np.zeros((6060600), dtype=np.float32)

Raw = np.zeros((1950, 16380), dtype=np.float32)

for x in range(3): data.readline()
for x in range(1950):
    line = data.readline().split(",")
    line.pop(0)
    line.pop(16382)
    line.pop(16381)
    line.pop(16380)
    for y in range(16380):
        if line[y] == "":
            Raw[x][y] = 0
        else:
            Raw[x][y] = float(line[y])

np.save("Raw.npy", Raw)

for day in range(5):
    for trial in range(370):
        for company in range(3276):
            for x in range(10):
                if Raw[day * 390 + trial + x + 1][company * 5] == 0 or Raw[day * 390 + trial + x][company * 5] == 0:
                    X[day * 1212120 + trial * 3276 + company][x][0] = 0
                    X[day * 1212120 + trial * 3276 + company][x][1] = 0
                else:
                    X[day * 1212120 + trial * 3276 + company][x][0] = (Raw[day * 390 + trial + x + 1][company * 5] -
                                                                       Raw[day * 390 + trial + x][company * 5]) / \
                                                                      Raw[day * 390 + trial + x][company * 5]
                    X[day * 1212120 + trial * 3276 + company][x][1] = Raw[day * 390 + trial + x][
                                                                          company * 5 + 4] / 1000000
invalid = 0
for x in X:
    if 0 in x:
        invalid += 1

print(invalid)