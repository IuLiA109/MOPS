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
        "contour_min_points": 150,
        "offset_y": 50,
        "offset_x": 10,
    }

    if cfg is None:
        cfg = default_cfg
    else:
        temp = default_cfg.copy()
        temp.update(cfg)
        cfg = temp

    if image is None or image.size == 0:
        return None

    h, w = image.shape[:2]
    original_image = image.copy()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    mblur = cv.medianBlur(gray, cfg["median_blur_ksize"])
    gblur = cv.GaussianBlur(mblur, (0, 0), cfg["gauss_sigma"])
    sharpen = cv.addWeighted(
        mblur, cfg["sharpen_weight_1"],
        gblur, cfg["sharpen_weight_2"],
        0
    )
    thresh = cv.adaptiveThreshold(
        sharpen,
        255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,
        cfg["adaptive_blocksize"],
        cfg["adaptive_C"]
    )

    median = np.median(thresh)
    lower = int(max(0, cfg["canny_lower_coef"] * median))
    upper = int(min(255, cfg["canny_upper_coef"] * median))
    edges = cv.Canny(thresh, lower, upper)

    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    xmin, ymin = np.inf, np.inf
    xmax, ymax = -np.inf, -np.inf
    found = False

    for c in contours:
        if len(c) > cfg["contour_min_points"]:
            pts = c.reshape(-1, 2)
            xmin = min(xmin, pts[:, 0].min())
            xmax = max(xmax, pts[:, 0].max())
            ymin = min(ymin, pts[:, 1].min())
            ymax = max(ymax, pts[:, 1].max())
            found = True

    if not found:
        return original_image

    xmin = int(max(0, xmin + cfg["offset_x"]))
    ymin = int(max(0, ymin + cfg["offset_y"]))
    xmax = int(min(w, xmax - cfg["offset_x"]))
    ymax = int(min(h, ymax - cfg["offset_y"]))
    if xmin >= xmax or ymin >= ymax:
        return original_image

    result = original_image[ymin:ymax, xmin:xmax].copy()
    if result.size == 0:
        return original_image

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
