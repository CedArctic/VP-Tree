# Imports
import random
import matplotlib.pyplot as plt
import utilities
from utilities import Node, Point, DQueue

# Constants
POINTS_NUMBER = 100  # Number of randomly generated points
NEIGHBORS_NUMBER = 5  # Number of neighbors to find


def devideAndConquer(points):
    # Check to end recursion: if points array is of size 0 - we are returning a leaf
    if len(points) == 1:
        return Node([points[0], 0])

    # Select a random point and remove it from the list
    point = random.choice(points)
    points.remove(point)

    # Calculate median distance of point and add it with the point into the local node.
    # Node data is in the form of [point, median]
    distances = []
    for p in points:
        distances.append(p.distance(point))
    distances.sort()
    if len(distances) % 2 == 0:
        median = 0.5 * (distances[int(len(distances) / 2) - 1] + distances[int(len(distances) / 2)])
    else:
        median = distances[int((len(distances) + 1) / 2) - 1]
    localNode = Node([point, median])

    # Add vantage points to plot
    ax.add_patch(
        plt.Circle((point.X, point.Y), median, color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)),
                   alpha=0.1))

    # Sort points into two new arrays: the ones within median range and ones outside.
    # Those with distance less than median go on the left
    leftPoints = []
    rightPoints = []
    for p in points:
        if point.distance(p) < median:
            leftPoints.append(p)
        else:
            rightPoints.append(p)

    # Recursively call on left and right child of node
    if len(leftPoints) == 0:
        localNode.left = None
    else:
        localNode.left = devideAndConquer(leftPoints)

    if len(rightPoints) == 0:
        localNode.right = None
    else:
        localNode.right = devideAndConquer(rightPoints)

    # Return local node
    return localNode


# Call searchTree to find the query's neighbors
def searchTree(startingNode):
    # This is the radius around the query defined by the distance of query-furthest current neighbor
    if neighbors.length() is not 0:
        searchRadius = neighbors.peek_distance()
    else:
        # This is just a big default radius just so it will be directly replaced the first time searchTree is called
        searchRadius = 999999

    # Check if startingNode can be a neighbor based on its distance to the query point and already recorded neighbors
    nodePoint = startingNode.data[0]
    distance = nodePoint.distance(query)
    if distance < searchRadius:
        neighbors.insert(nodePoint, distance)
        # Update searchRadius after adding a neighbor
        searchRadius = neighbors.peek_distance()

    # First search by scaling down the tree following the left or right subtree each time according to the query's
    # distance to the subtree root node.
    # Also check if we should check the other subtree by checking if the other subtree root intersects with the maximum
    # radius around the query. This decision is made after we have completely scaled down the tree.

    # NodePointRadius is the radius around the nodePoint defined by the median of points around it
    nodePointRadius = startingNode.data[1]

    # If nodePointRadius is 0 it means we've reached a leaf in the binary tree so we end the recursion
    if nodePointRadius == 0:
        return

    # In this case the query point is within the nodePointRadius so we scale down the left subtree and decide if we also
    # want to search the right subtree of the startingNode.
    if (distance < nodePointRadius) and (startingNode.left is not None):
        searchTree(startingNode.left)

        # If this is true, it means that part of the search area around our query point intersects with the area outside
        # of the one covered by the left subtree. We refresh the searchRadius variable because it is possible that it
        # has been updated while searchTree(startingNode.left). We also test that the other subtree exists.
        searchRadius = neighbors.peek_distance()
        if (nodePointRadius < (distance + searchRadius)) and (startingNode.right is not None):
            searchTree(startingNode.right)

    # In this case the query point is outside the nodePointRadius so we scale down the right subtree and decide if we
    # also want to search the left subtree of the startingNode
    elif (distance >= nodePointRadius) and (startingNode.right is not None):
        searchTree(startingNode.right)

        # If this is true, it means that part of the search area around our query point intersects with the area outside
        # of the one covered by the right subtree. We refresh the searchRadius variable because it is possible that it
        # has been updated while searchTree(startingNode.left). We also test that the other subtree exists.
        searchRadius = neighbors.peek_distance()
        if (distance < (nodePointRadius + searchRadius)) and (startingNode.left is not None):
            searchTree(startingNode.left)
    else:
        return


# Main program

# Setup plot
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])

# Generate random points on a two dimensional plane
points = utilities.random_points(POINTS_NUMBER)

# Nodes contain the point and its median distance from all other points in the format Node([ point, median])
# Call devideAndConquer to build the binary tree
root = devideAndConquer(points)

# Generate a random point to use as a query
query = Point(random.random(), random.random())

# Call searchTree to find the query's neighbors
neighbors = DQueue(NEIGHBORS_NUMBER)
searchTree(root)

# Print results and make the plot
print("Query Point: \n")
query.print()
ax.plot(query.X, query.Y, 'bo')
print("Neighbors: ")
for point in points:
    ax.plot(point.X, point.Y, 'ro')
for neighbor in neighbors.data:
    neighbor[0].print()
    ax.plot(neighbor[0].X, neighbor[0].Y, 'go')

plt.show()
