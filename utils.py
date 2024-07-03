import cv2
import numpy as np
from all_bubbles import get_all_bubbles




def crop_image(image):
    y_crop_start = int(image.shape[0] * 0.238)
    y_crop_end = int(image.shape[0] - (image.shape[0] * 0.027))
    x_crop_start = int(image.shape[1] * 0.043)
    x_crop_end = int(image.shape[1]  - (image.shape[1] * 0.069))
    cropped = image[y_crop_start:y_crop_end, x_crop_start:x_crop_end]
    return cropped

def crop_cords(image):
    y_crop_start = int(image.shape[0] * 0.234)
    y_crop_end = int(image.shape[0] - (image.shape[0] * 0.027))
    x_crop_start = int(image.shape[1] * 0.043)
    x_crop_end = int(image.shape[1]  - (image.shape[1] * 0.069))
    return (y_crop_start, y_crop_end, x_crop_start, x_crop_end)


def get_coloumns(image):
    cropped = crop_image(image)
    coloumns = []
    part = int(cropped.shape[1]/6)
    const_row = cropped.shape[0]
    for i in range(1,7):
        start = (i - 1) * part
        end = i * part
        coloumns.append(cropped[0:const_row, start:end])
    return coloumns


def get_rows(image):
    rows = []
    part = int(image.shape[0]/5)
    const_col = image.shape[1]
    for i in range(1,6):
        start = (i - 1) * part
        end = i * part
        rows.append(image[start:end , 0:const_col])
    return rows




def standard_resize(image, n):
    ims = cv2.resize(image, (int(image.shape[1]/n),int(image.shape[0]/n)))
    return ims


def find_quarter(shape, contour):
    quarter = shape[1]/4
    start = contour[0][0][0]
    if start < quarter * 1:
        return "A"
    elif start < quarter * 2:
        return "B"
    elif start < quarter * 3:
        return "C"
    elif start < quarter * 4:
        return "D"
    


def find_bubbles_from_contour(contours):
    bubbles = []
    for contour in contours:
        
        area = cv2.contourArea(contour)
        
        
        perimeter = cv2.arcLength(contour, True)
        
        
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        
        if hull_area > 0:
            solidity = float(area) / hull_area
        else:
            solidity = 0
        
        
        if area > 670 and solidity > 0.9:
            
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
            else:
                continue
            
            
            bubbles.append(contour)
    return bubbles




def have_common_y(contour1, contour2):
   
    
    x1, y1, w1, h1 = cv2.boundingRect(contour1)
    x2, y2, w2, h2 = cv2.boundingRect(contour2)
    
    
    y_range1 = (y1, y1 + h1)
    y_range2 = (y2, y2 + h2)
    
    
    if y_range1[1] >= y_range2[0] and y_range1[0] <= y_range2[1]:
        return True
    return False



def distance_between_contours(contour1, contour2):
    
    x1, y1, w1, h1 = cv2.boundingRect(contour1)
    x2, y2, w2, h2 = cv2.boundingRect(contour2)
    
    n1 = (y1 + h1)/2
    n2 = (y2 + h2)/2
    
    
    distance = n2 - n1
    return distance


def contours_in_range_y(start, end, bubble,contours, image):
    count = 0
    filter_contour = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if y < start:
            continue
        
        if y + h > end:
            break
        count = count + 1
        filter_contour.append(contour)
    #cv2.drawContours(image, filter_contour, -1, (255, 0, 255), 6)

    return count




def mixed_bubbles(contours, contour):
    areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 1000]
    avg = np.average(areas)


    if cv2.contourArea(contour) > avg * 1.6:
        return True
    return False






def find_bubbles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray, (5, 5), 0)


    _, binary_image = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)
    closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=1)


    opened_image = cv2.morphologyEx(closed_image, cv2.MORPH_OPEN, kernel, iterations=5)

    """cv2.imshow("fff", opened_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    contours, _ = cv2.findContours(opened_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    

    #cv2.drawContours(image, contours, -1, (255, 0, 255), 6)


    bubbles = find_bubbles_from_contour(contours)
    
    
    return contours



def image_slice(image, x_start, x_end, y_start, y_end):
    new_image = image[y_start:y_end, x_start:x_end]
    return new_image




def find_choices(image, row, col, height_part, width_part, main_image):
    choices = []
    bubbles = find_bubbles(image)
    rev_bubbles = reversed(bubbles)
    i = 1


    #cv2.drawContours(image, bubbles, -1, (255, 0, 255), 6)
    
    


    


    thresold = (image.shape[0]/15) 
    



    last_bubble = None
    for bubble in rev_bubbles:
        cv2.drawContours(image, bubble, -1, (255, 0, 255), 6)

        if last_bubble is None:
			
            _, bound, _, _ = cv2.boundingRect(bubble)
            
            contours = get_all_bubbles(image)
            for j in range(contours_in_range_y(0,bound , bubble,contours, image)):
                choices.append(0)
                i = i + 1
            
            choices.append(find_quarter(image.shape,bubble))
            last_bubble = bubble
            i = i + 1
            continue
        
        
        if have_common_y(last_bubble, bubble):
            last_bubble = bubble
            
            continue
        dis = distance_between_contours(last_bubble, bubble)
        
        if dis > thresold:
            _, start, _, w = cv2.boundingRect(last_bubble)
            _, end, _, h = cv2.boundingRect(bubble)
            
            for j in range(contours_in_range_y(start + w + (w/6), end, bubble,contours, image)):
                choices.append(0)
                i = i + 1
            
            
        choices.append(find_quarter(image.shape,bubble))
        last_bubble = bubble
        
        i = i + 1
        
    while i < 11:
        choices.append(0)
        i = i + 1



    return choices



def get_bubble(bubbles, i):
    j = 1
    reversed_b = reversed(bubbles)
    for bubble in reversed_b:
        if j == i :
            return bubble
        j = j + 1
    
    return None


def highlight_errors(row, choices, bubbles, answers, n, m):
    i = 1
    j = 1
    report_data = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    for choice in choices:
        answer_index =(m * 50) + (n * 10) + i
        question = answer_index
        correct_anwer = answers[answer_index]
        student_answer = choice
        correct = False
        if answer_index > 150:
            break
        if choice == 0 :
            correct = False
            i = i + 1
            report_data.append({
            'question': question,
            'correct_answer': correct_anwer,
            'student_answer': student_answer,
            'correct': correct,
            })
            continue
        
        if choice == answers[answer_index]:
            cv2.drawContours(row, [get_bubble(bubbles, j)], -1, (0, 255, 0), 2)
            correct = True
            
        else:
            cv2.drawContours(row, [get_bubble(bubbles, j)], -1, (0, 0, 255), 2)
            correct = False
            
        M = cv2.moments(get_bubble(bubbles, j))
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            continue
        
        
        cv2.putText(row, (f"{choice}-{answer_index}") , (cX - 30, cY - 10), font, 0.5, (255, 0, 0), 2)

        
        report_data.append({
            'question': question,
            'correct_answer': correct_anwer,
            'student_answer': student_answer,
            'correct': correct,
        })

        i = i + 1
        j = j + 1
    
    
    return row, report_data




def score_from_report(report):
    score = 0
    for r in report:
        if r['correct']:
            score = score + 1

    return score



