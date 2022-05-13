from sklearn.cluster import DBSCAN
import numpy as np
import re
import matplotlib.pyplot as plt

RECT_SIZE = 1
RADIUS = 0.5
EPS = 8
MIN_SAMPLES = 30
USE_START_POINTS = False
SUCCESFUL_EXIT = False

if SUCCESFUL_EXIT:
    INFO = "Success controlled exit." + (" Start points" if USE_START_POINTS else " Stop points")
    NAME_OF_FILE = "success_cluster_start_pts" if USE_START_POINTS else "success_cluster_stop_pts"
else:
    INFO = "Fail controlled exit." + (" Start points" if USE_START_POINTS else " Stop points")
    NAME_OF_FILE = "fail_cluster_start_pts" if USE_START_POINTS else "fail_cluster_stop_pts"
COLORS = ["yellow","purple", "black", "brown", "green", "blue", "orange", "red"]

if SUCCESFUL_EXIT:
    DataFile = "successful_control_exit.csv"
else:
    DataFile = "fail_control_exit.csv"

if USE_START_POINTS:
    DataCaptured = open(DataFile)
    x = []
    y = []
    label = []
    for row in DataCaptured:
        s = re.split(r';', row)
        x.append(float(s[0]))
        x.append(float(s[2]))
        y.append(float(s[1]))
        y.append(float(s[3]))
        label.append(s[4])
        label.append(s[4])
        start_points = []
        stop_points = []
        for i in range(0, len(x), 2):
            x1, x2 = x[i: i + 2]
            y1, y2 = y[i: i + 2]
            start_points.append([x1, y1])
            stop_points.append([x2, y2])
    X = np.array([i for i in start_points])

    # min samples is like min neighours
    # eps is size of radius
    dbscan = DBSCAN(eps = EPS, min_samples = MIN_SAMPLES)

    model = dbscan.fit(X)
    myset = set()
    for i in model.labels_:
        myset.add(i)
    clusters = []
    colors = []

    for i in myset:
        if i == -1:
            continue
        clusters.append(i)
        colors.append(COLORS.pop(-1))

    clusters.append(-1)
    print(f"Length of set: {len(clusters)}\nActual set:{clusters}")
    print(model.labels_.shape) # same as input data

    for i in range(0, len(start_points)):
        # plt.plot(x[i:i + 2], y[i:i + 2], 'g.-' if label[i] == "1" else 'r.-', linewidth = 0.1, markersize=2)
        x1, y1 = start_points[i]
        rectangle = plt.Rectangle((x1, y1), RECT_SIZE, RECT_SIZE, fc="gray" if model.labels_[i] == -1 else colors[model.labels_[i]])
        plt.gca().add_patch(rectangle)
        # circle = plt.Circle((x2, y2), RADIUS, fc='green' if label[i] == '1' else 'red')
        # plt.gca().add_patch(circle)
    plt.title(f"{INFO} clustered. Eps={EPS}, min_samples={MIN_SAMPLES}")
    plt.axis('scaled')
    plt.savefig("../plot/" + NAME_OF_FILE, dpi=300)
    plt.show()
else:
    DataCaptured = open(DataFile)
    x = []
    y = []
    label = []
    for row in DataCaptured:
        s = re.split(r';', row)
        x.append(float(s[0]))
        x.append(float(s[2]))
        y.append(float(s[1]))
        y.append(float(s[3]))
        label.append(s[4])
        label.append(s[4])
        start_points = []
        stop_points = []
        for i in range(0, len(x), 2):
            x1, x2 = x[i: i + 2]
            y1, y2 = y[i: i + 2]
            start_points.append([x1, y1])
            stop_points.append([x2, y2])
    X = np.array([i for i in stop_points])

    # min samples is like min neighours
    # eps is size of radius
    dbscan = DBSCAN(eps = EPS, min_samples = MIN_SAMPLES)

    model = dbscan.fit(X)
    myset = set()
    for i in model.labels_:
        myset.add(i)
    clusters = []
    # Need 4 colours
    colors = []
    for i in myset:
        if i == -1:
            continue
        clusters.append(i)
        colors.append(COLORS.pop(-1))

    clusters.append(-1)
    print(f"Length of set: {len(clusters)}\nActual set:{clusters}")
    print(model.labels_.shape) # same as input data

    for i in range(0, len(stop_points)):
        # plt.plot(x[i:i + 2], y[i:i + 2], 'g.-' if label[i] == "1" else 'r.-', linewidth = 0.1, markersize=2)
        x1, y1 = stop_points[i]
        rectangle = plt.Rectangle((x1, y1), RECT_SIZE, RECT_SIZE, fc="gray" if model.labels_[i] == -1 else colors[model.labels_[i]])
        plt.gca().add_patch(rectangle)
        # circle = plt.Circle((x2, y2), RADIUS, fc='green' if label[i] == '1' else 'red')
        # plt.gca().add_patch(circle)
    plt.title(f"{INFO} clustered. Eps={EPS}, min_samples={MIN_SAMPLES}")
    plt.axis('scaled')
    plt.savefig("../plot/" + NAME_OF_FILE, dpi=300)
    plt.show()