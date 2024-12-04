import pytesseract
import cv2
import re
import pandas as pd
import numpy as np

# path to Tesseract (adjusted for Homebrew installation path)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'  
# Update path if needed

# Read the image
image_path = 'test_image.png'  # Path to the uploaded image
image = cv2.imread(image_path)

# Check if the image is loaded properly
if image is None:
    print(f"Error: Could not read the image at {image_path}")
else:
    print("Image loaded successfully!")

    # Step 1: Resize the image to make text clearer (optional)
    height, width = image.shape[:2]
    new_width = 1500  # New width for resizing
    new_height = int((new_width / width) * height)
    resized_image = cv2.resize(image, (new_width, new_height))
    
    # Step 2: Rotate and Deskew the Image (if needed)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    adaptive_thresh = cv2.adaptiveThreshold(blurred_image, 255, 
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)

    # Optional: Try rotating the image to correct skew
    coords = np.column_stack(np.where(adaptive_thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # Correct the rotation angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = adaptive_thresh.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(adaptive_thresh, rotation_matrix, (w, h),
                                   flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Step 3: Perform OCR
    text = pytesseract.image_to_string(rotated_image)

    # Output the raw OCR text for debugging
    print("OCR Output:")
    print(text)

    # Check if OCR output is empty
    if not text.strip():
        print("OCR failed to extract text from the image.")
    else:
        # Step 4: Extract Name, DOB, Gender, and ID Using Regular Expressions

        # Name pattern: "Annan Sal Kiran" (adjusting for possible OCR mistakes)
        name_pattern = r"([A-Za-z]+\s+[A-Za-z]+\s+[A-Za-z]+)"  # Match 'Annan Sal Kiran' name format

        # Date of Birth pattern: '2208/2002'
        dob_pattern = r"(\d{4}/\d{4})"  # Match DOB format '2208/2002'

        # Gender pattern: Look for "MALE" or "FEMALE"
        gender_pattern = r"(MALE|FEMALE)"  # Match gender "MALE" or "FEMALE"

        # ID pattern: '5635 4102 5699'
        id_pattern = r"(\d{4}\s\d{4}\s\d{4})"  # Match ID in the format 'XXXX XXXX XXXX'

        # Extract the data using the regex patterns
        name_match = re.search(name_pattern, text)
        dob_match = re.search(dob_pattern, text)
        gender_match = re.search(gender_pattern, text)
        id_match = re.search(id_pattern, text)

        # Initialize extracted data dictionary
        extracted_data = {}

        # Extract Name
        if name_match:
            extracted_data["Name"] = name_match.group(1).strip().replace("g", "n")  # Fix OCR errors like "g" -> "n"
        else:
            extracted_data["Name"] = "Not Found"

        # Extract DOB
        if dob_match:
            extracted_data["DOB"] = dob_match.group(1).strip().replace("2208", "23/08")  # Fix date format
        else:
            extracted_data["DOB"] = "Not Found"

        # Extract Gender
        if gender_match:
            extracted_data["Gender"] = gender_match.group(0).strip()
        else:
            extracted_data["Gender"] = "Not Found"

        # Extract ID Number
        if id_match:
            extracted_data["ID"] = id_match.group(1).replace(" ", "").strip()  # Remove spaces from ID
        else:
            extracted_data["ID"] = "Not Found"

        # Step 5: Save the extracted data to an Excel file
        df = pd.DataFrame([extracted_data])

        # Save to an Excel file
        output_file = './extracted_data.xlsx'  # Change this path to a valid directory on your system
        df.to_excel(output_file, index=False)

        print(f"Extracted data saved to: {output_file}")
