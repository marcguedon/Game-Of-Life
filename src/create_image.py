import cv2
from utils import from_pattern_to_image

pattern = [[1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]]

image = from_pattern_to_image(pattern)
cv2.imshow("Pattern", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
