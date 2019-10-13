# Imports
import random, math


# Generates an array of random points on a two dimensional plane
def random_points(pointsNum):
    a = []
    for i in range(0, pointsNum):
        a.append(Point(random.random(), random.random()))
    return a


# Base class for a point
class Point:

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    # Calculate distance between two points
    def distance(self, otherPoint):
        return math.sqrt(pow((self.X - otherPoint.X), 2)
                         + pow((self.Y - otherPoint.Y), 2))

    def print(self):
        print("Point (X,Y): " + str(self.X) + ", " + str(self.Y) + "\n")


# Base class for a binary tree
class Node:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    # Print the tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()


# Base class for a queu that will hold points and their distance to the query and be ordered by distance
class DQueue:

    def __init__(self, maxLength):
        self.data = []
        self.maxLength = maxLength

    # Returns number of elements currently in the DQueue
    def length(self):
        return len(self.data)

    # Insert DQueue element ([point, distance]) based on distance
    def insert(self, point, distance):
        index = 0
        if self.length() > 0:
            while self.data[index][1] < distance:
                index += 1
        self.data.insert(index, [point, distance])
        # Shave off excess elements
        del self.data[self.maxLength:]

    # Peek the distance of the last element - the one furthest away based on distance
    def peek_distance(self):
        return self.data[self.length()-1][1];
