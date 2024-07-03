import cv2
import numpy as np
import os
import pandas as pd
from utils import get_coloumns,get_rows,find_choices, highlight_errors, find_bubbles,score_from_report
from answers import master_answers
from student import get_id
sheets_path = 'sheets/'
all_reports = []
student_index = 0
for file_name in os.listdir(sheets_path):
    
    file_path = os.path.join(sheets_path, file_name)
    

    image = cv2.imread(file_path)
    id = get_id(image)
    
    coloumns = get_coloumns(image)
    rows = get_rows(coloumns[0])
    whole_shape = (rows[0].shape[0] * 5, coloumns[0].shape[1] * 3)

    whole_image = np.zeros((rows[0].shape[0] * 5, coloumns[0].shape[1] * 3, 3), dtype=np.uint8)

    width_part = coloumns[0].shape[1]
    height_part = rows[0].shape[0]
    image_parts = []
    report_data = []
    all_choices = []
    for i in range(3):
        coloumns = get_coloumns(image)
        for j in range(5):
            choices = []
            rows = get_rows(coloumns[i])
            row = rows[j]
            bubbles = find_bubbles(row)
            choices = find_choices(row,j, i, height_part, width_part, image)
            highlighted_row , data= highlight_errors(row, choices,find_bubbles(row),master_answers,j, i)
            report_data.extend(data)
            all_choices.extend(choices)
            whole_image[(j * height_part):((j + 1) * height_part), (i * width_part):((i + 1) * width_part)] = row
        image_parts.append(rows)
    cv2.imwrite(f'transcripts/transcript_{id}.jpg', image)
    
    all_reports.append({
        'id': id,
        'score': score_from_report(report_data)
    })
    df = pd.DataFrame(report_data)
    df.to_excel(f'reports/student_{id}_report.xlsx', index=False)
    student_index = student_index + 1

summary_df = pd.DataFrame(all_reports)
summary_df.to_excel(f'reports/summary_report.xlsx', index=False)





