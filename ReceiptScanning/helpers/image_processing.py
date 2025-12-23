import cv2 as cv
import numpy as np
import pytesseract

def show_image(title,image):
    image=cv.resize(image,(0,0),fx=0.8,fy=0.8)
    cv.imshow(title,image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def extrage_bon(image, cfg=None):

    default_cfg = {
        "median_blur_ksize": 15,         
        "gauss_sigma": 75,               
        "sharpen_weight_1": 1.4,         
        "sharpen_weight_2": -0.9,       
        "threshold_value": 30,           
        "adaptive_blocksize": 11,       
        "adaptive_C": 2,                
        "erode_kernel_size": 3,          
        "erode_iterations": 1,           
        "canny_lower_coef": 0.67,        
        "canny_upper_coef": 1.33,        
        "contour_min_points": 150        
    }

    if cfg is None:
        cfg = default_cfg
    else:
        temp = default_cfg.copy()
        temp.update(cfg)
        cfg = temp

    original_image = image.copy()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    mblur = cv.medianBlur(gray, cfg["median_blur_ksize"])
    gblur = cv.GaussianBlur(mblur, (0, 0), cfg["gauss_sigma"])
    sharpen = cv.addWeighted(
        mblur,
        cfg["sharpen_weight_1"],
        gblur,
        cfg["sharpen_weight_2"],
        0
    )

    _, thresh = cv.threshold(sharpen, cfg["threshold_value"], 255, cv.THRESH_BINARY)
    kernel = np.ones((cfg["erode_kernel_size"], cfg["erode_kernel_size"]), np.uint8)
    thresh = cv.erode(thresh, kernel, iterations=cfg["erode_iterations"])
    thresh = cv.adaptiveThreshold(
        sharpen,
        255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,
        cfg["adaptive_blocksize"],
        cfg["adaptive_C"]
    )

    # show_image("thresh", thresh)

    median = np.median(thresh)
    lower = int(max(0, cfg["canny_lower_coef"] * median))
    upper = int(min(255, cfg["canny_upper_coef"] * median))
    edges = cv.Canny(thresh, lower, upper)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    xmin = 10000000
    ymin = 10000000
    xmax = 0
    ymax = 0

    for i in range(len(contours)):
        if (len(contours[i]) > cfg["contour_min_points"]):
            for point in contours[i].squeeze():
                if point[0] < xmin:
                    xmin = point[0]

                if point[0] > xmax:
                    xmax = point[0]

                if point[1] < ymin:
                    ymin = point[1]

                if point[1] > ymax:
                    ymax = point[1]

    image_marked = original_image.copy()

    cv.circle(image_marked, (xmin, ymin), 20, (0, 0, 255), -1)  
    cv.circle(image_marked, (xmax, ymin), 20, (0, 255, 0), -1)  
    cv.circle(image_marked, (xmax, ymax), 20, (255, 0, 0), -1)  
    cv.circle(image_marked, (xmin, ymax), 20, (0, 255, 255), -1) 

    # cv.imshow("colturi detectate", image_marked)
    cv.waitKey(0)

    offset_y = 50 
    ymin_offset = ymin + offset_y
    ymax_offset = ymax - offset_y
    offset_x = 10 
    xmin_offset = xmin + offset_x
    xmax_offset = xmax - offset_x

    result = original_image[ymin_offset:ymax_offset, xmin_offset:xmax_offset].copy()
    return result

def preprocesare_generala(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    scale = 2.0
    w = int(gray.shape[1] * scale)
    h = int(gray.shape[0] * scale)
    resized = cv.resize(gray, (w, h), interpolation=cv.INTER_CUBIC)
    denoised = cv.bilateralFilter(resized, 9, 50, 50)
    kernel_reparare = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    repaired = cv.morphologyEx(denoised, cv.MORPH_CLOSE, kernel_reparare)

    binary = cv.adaptiveThreshold(
        repaired,                      
        255, 
        cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv.THRESH_BINARY_INV, 
        31,                            
        4                
    )
    return resized, binary

def extrage_linii_text(gray_image, binary_image):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (30, 1))
    dilated = cv.dilate(binary_image, kernel, iterations=1)
    
    projection = np.sum(dilated, axis=1)
    lines = []
    start = -1
    threshold = 10 
    
    for y, val in enumerate(projection):
        if val > threshold and start == -1:
            start = y
        elif val <= threshold and start != -1:
            end = y
            if end - start > 15: 
                lines.append((max(0, start-2), min(binary_image.shape[0], end+2)))
            start = -1
            
    if start != -1:
        lines.append((start, binary_image.shape[0]))

    slices = []
    for (y1, y2) in lines:
        roi = gray_image[y1:y2, :]
        roi_padded = cv.copyMakeBorder(
            roi, 10, 10, 10, 10, cv.BORDER_CONSTANT, value=(255, 255, 255)
        )
        slices.append(roi_padded)
        
    return slices

def proceseaza_linie_ocr(img_linie):
    config = "--psm 6"
    _, bw = cv.threshold(img_linie, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    text = pytesseract.image_to_string(bw, lang='ron+eng', config=config)
    return text.strip()
