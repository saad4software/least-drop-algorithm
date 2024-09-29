import networkx as nx
import cv2
import math

def find_min_drop_path(image, start_pixel, end_pixel):
  img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  image = img_hsv[..., 0]

  # Create a graph from the image (assuming image is a NumPy array)
  G = nx.Graph()
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      G.add_node((i, j))
      if i > 0:
        diff = abs(int(image[i-1, j]) - int(image[i, j]))
        diff = min(diff,180-diff)
        G.add_edge((i, j), (i-1, j), weight= diff if diff >0 else 0)
      if j > 0:
        diff = abs(int(image[i, j-1]) - int(image[i, j]))
        diff = min(diff,180-diff)
        G.add_edge((i, j), (i, j-1), weight= diff if diff>0 else 0)

  # Find the shortest path using Dijkstra's algorithm
  path = nx.dijkstra_path(G, start_pixel, end_pixel, weight='weight')

  return path


def onMouse(event, x, y, flags, param):
  global points
  if event == cv2.EVENT_LBUTTONDOWN:
    print('x = %d, y = %d'%(x, y))
    cv2.circle(img, (x, y), 1,(255,0,255))
    cv2.imshow("map", img)
    points += [(y, x)]


points = []

if __name__ == '__main__':

  img = cv2.imread("elevation-maps/lovers-channel.jpg")



  cv2.imshow("map", img)
  cv2.setMouseCallback('map', onMouse)
  
  print("Please select the start and end points then click any key")
  cv2.waitKey(0)


  if len(points) == 2:
    path = find_min_drop_path(img, points[0], points[1])
    for point in path:
      cv2.circle(img, (point[1], point[0]), 1,(0,0,255))

  cv2.imshow("map", img)
  cv2.waitKey(0)
