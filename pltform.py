import time
import math
import numpy as np
import matplotlib.pyplot as plt
def rotate(object, ax, ay, az):
    ax = math.radians(ax)
    ay = math.radians(ay)
    az = math.radians(az)
    robject = []
    for j in range(len(object)):
        rpoints = []
        for point in object[j]:
            point = np.array(point)
            rotx = np.array(
                [[1, 0, 0],
                [0, math.cos(ax), -math.sin(ax)],
                [0, math.sin(ax), math.cos(ax)]])
            roty = np.array(
                [[math.cos(ay), 0, math.sin(ay)],
                [0, 1, 0],
                [-math.sin(ay), 0, math.cos(ay)]])
            rotz = np.array(
                [[math.cos(az), -math.sin(az), 0],
                [math.sin(az), math.cos(az), 0],
                [0, 0, 1]])
            rpoint = tuple(rotz @ roty @ rotx @ point)
            rpoints.append(rpoint)
        robject.append(rpoints)
    return robject
def translate(object, tx, ty, tz):
    tobject = []
    for j in range(len(object)):
        tpoints = []
        for point in object[j]:
            point = np.array(point)
            tpoint = tuple(point + np.array([tx, ty, tz]))
            tpoints.append(tpoint)
        tobject.append(tpoints)
    return tobject
def scale(object, sx, sy, sz):
    sobject = []
    for j in range(len(object)):
        spoints = []
        for point in object[j]:
            point = np.array(point)
            spoint = tuple(point * np.array([sx, sy, sz]))
            spoints.append(spoint)
        sobject.append(spoints)
    return sobject
def plot(object, type = '', equal = False):
    if equal:
        plt.axis('equal')
    for points in object:
        xvals = [point[0] for point in points] + [points[0][0]]
        yvals = [point[1] for point in points] + [points[0][1]]
        if type == '':
            plt.plot(xvals, yvals)
        else:
            plt.plot(xvals, yvals, type)
def show():
    plt.show()
def pause(t):
    plt.pause(t)
def clf():
    plt.clf()
def openobj(filename):
    vertices = []
    obj = []
    with open(filename, 'r') as file:
        for line in file:
            if not line or line.startswith('#'):
                continue
            parts = line.strip().split()
            if parts[0] == 'v':
                vertices.append((
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3])
                ))
            elif parts[0] == 'f':
                face = []
                for vert in parts[1:]:
                    idx = int(vert.split('/')[0]) - 1
                    face.append(vertices[idx])
                obj.append(face)
    return obj
def exportobj(points, path):
    vertexmap = {}
    vertices = []
    elements = []
    def getindex(v):
        if v not in vertexmap:
            vertexmap[v] = len(vertices) + 1
            vertices.append(v)
        return vertexmap[v]
    for elem in points:
        if not elem:
            continue
        indices = [getindex(v) for v in elem]
        if len(indices) == 1:
            elements.append(('p', indices))
        elif len(indices) == 2:
            elements.append(('l', indices))
        else:
            elements.append(('f', indices))
    with open(path, 'w') as f:
        for v in vertices:
            f.write(f'v {v[0]} {v[1]} {v[2]}\n')
        for kind, idxs in elements:
            f.write(kind + ' ' + ' '.join(map(str, idxs)) + '\n')