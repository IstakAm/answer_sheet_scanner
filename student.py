import cv2
import numpy as np


def get_id(image):
    x_start = int(image.shape[1] * 0.412)
    x_end = int(image.shape[1] * 0.923)
    y_start = int(image.shape[0] * 0.054)
    y_end = int(image.shape[0] * 0.242)

    
    main_image = image.copy()[y_start:y_end, x_start:x_end]


    blur = cv2.medianBlur(main_image, 3)

    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    _ , binary_image = cv2.threshold(gray, 115, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=5)


    opened_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, kernel, iterations=1)


    contours, _ = cv2.findContours(opened_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    bubbles = [c for c in contours if cv2.contourArea(c) < 2000]

    limits = []
    starts = []


    bounding_rects = [(bubble, cv2.boundingRect(bubble)) for bubble in bubbles]


    sorted_bounding_rects = sorted(bounding_rects, key=lambda x: x[1][0])

    sorted_bubbles = [contour for contour, _ in sorted_bounding_rects]


    bubbles = sorted_bubbles

    for b in bubbles:
        _, y, _, h = cv2.boundingRect(b)
        limits.append(h)
        starts.append(y)

    avg = np.average(limits) + 8.2
    min_y = min(starts)

    id = ""



    for i in starts:
        if (i - min_y) < avg :
            id = id + "0"
        else :
            id = id + str(round(abs(( i - min_y)/avg)))

    return id

