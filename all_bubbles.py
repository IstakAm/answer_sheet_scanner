import cv2

import numpy as np



def get_all_bubbles(image):
    

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    edges = cv2.Canny(gray, 100, 5)


    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(c) for c in contours]
    avg = np.average(areas)
    
    f_contours = [c for c in contours if cv2.contourArea(c) > avg/3]

    def is_round(contour, tol=0.7):
        
        (x, y), radius = cv2.minEnclosingCircle(contour)
        
        
        if radius > 0:
            contour_area = cv2.contourArea(contour)
            circle_area = np.pi * (radius ** 2)

            
            if abs(contour_area - circle_area) / circle_area < tol and  cv2.contourArea(contour) > avg/2:
                return True
        return False


    round_contours = [contour for contour in f_contours if is_round(contour)]
    

    sorted_round_contours = sorted(round_contours, key=lambda contour: cv2.boundingRect(contour)[1])

    def y_overlap(rect1, rect2):
        y1, h1 = rect1[1], rect1[3]
        y2, h2 = rect2[1], rect2[3]
        return not (y1 + h1 < y2 or y2 + h2 < y1)


    filtered_contours = []
    filtered_bounding_boxes = []
    final_contours = []
    i = 0

    while i < len(sorted_round_contours):
        keep_contour = sorted_round_contours[i]
        keep_rect = cv2.boundingRect(keep_contour)
        j = i + 1
        while j < len(sorted_round_contours):
            next_contour = sorted_round_contours[j]
            next_rect = cv2.boundingRect(next_contour)
            if y_overlap(keep_rect, next_rect):
                # Compare areas and keep the larger one
                area1 = cv2.contourArea(keep_contour)
                area2 = cv2.contourArea(next_contour)
                if area1 < area2:
                    keep_contour = next_contour  # Update to keep the larger contour
                    keep_rect = next_rect
            j += 1
        
        # Add the kept contour and its bounding box if it's not already in the filtered list
        if keep_rect not in filtered_bounding_boxes:
            filtered_contours.append(keep_contour)
            filtered_bounding_boxes.append(keep_rect)
        
        # Skip all contours that overlap with the current kept contour
        overlap_detected = False
        while i < len(sorted_round_contours) and y_overlap(keep_rect, cv2.boundingRect(sorted_round_contours[i])):
            i += 1
            overlap_detected = True

        # If no overlap was detected, increment i to avoid infinite loop
        if not overlap_detected:
            i += 1

    areas = [cv2.contourArea(c) for c in filtered_contours]
    aveg = np.average(areas)
    for contour in filtered_contours:
        if cv2.contourArea(contour) > aveg/2:
            final_contours.append(contour)
    #cv2.drawContours(image, final_contours, -1, (255, 0, 255), 2)
    
    return final_contours




