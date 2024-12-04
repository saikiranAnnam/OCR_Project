# OCR Text Extraction

This Python script utilizes Optical Character Recognition (OCR) to extract and process text data from an image. It focuses on extracting key personal information, such as Name, Date of Birth (DOB), Gender, and ID Number, using regular expressions (regex) to match patterns in the OCR output. Finally, the extracted data is saved in an Excel file for further use.

## Requirements

To run this script, ensure you have the following dependencies installed:

- Python 3.x
- `pytesseract` - Python wrapper for Tesseract OCR
- `opencv-python` - OpenCV for image processing
- `pandas` - Data handling and saving to Excel
- `numpy` - For numerical operations

### Installation

You can install the necessary dependencies using `pip`:

```bash
pip install pytesseract opencv-python pandas numpy
```

Additionally, ensure that Tesseract is installed on your system:

#### For macOS (using Homebrew):
```bash
brew install tesseract
```

If you're on a different operating system, follow the instructions from the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract) to install it.

## Script Overview

The script performs the following steps:

### 1. **Image Loading and Resizing**
   - The script reads an image file (`test_image.png`) and checks if it is loaded successfully.
   - It then resizes the image to make the text clearer for OCR extraction.

### 2. **Preprocessing: Rotation and Deskewing**
   - Converts the image to grayscale.
   - Applies Gaussian blur to reduce noise.
   - Uses adaptive thresholding to enhance text features.
   - Optionally rotates the image to correct any skew.

### 3. **Text Extraction Using OCR**
   - The Tesseract OCR engine is used to extract text from the processed image.
   - The OCR output is printed for inspection.

### 4. **Data Extraction Using Regular Expressions**
   - The extracted text is parsed to find key pieces of information:
     - **Name**: Matches a pattern of "Firstname Middlename Lastname".
     - **Date of Birth (DOB)**: Matches dates formatted as `DDMM/YYYY`.
     - **Gender**: Matches "MALE" or "FEMALE".
     - **ID Number**: Matches ID numbers in the format `XXXX XXXX XXXX`.
   - OCR errors are addressed using string replacements and adjustments in the regular expressions.

### 5. **Saving the Data**
   - The extracted data is saved into a dictionary.
   - The dictionary is written to an Excel file (`extracted_data.xlsx`) using the `pandas` library.

## How to Run

1. **Install dependencies**: Follow the installation instructions above to install the necessary libraries.
2. **Prepare the image**: Place the image you want to extract text from in the same directory as this script or adjust the `image_path` to point to the correct location.
3. **Run the script**: Execute the script using Python:

   ```bash
   python main.py
   ```

4. **Output**: The script will output the extracted text in the console and save the parsed data in an Excel file (`extracted_data.xlsx`).

## Notes

- Make sure Tesseract OCR is installed and the path (`tesseract_cmd`) is correctly set in the script.
- The script assumes that the image contains clear text with minimal noise or distortion. Adjustments to preprocessing might be required for images with more complex backgrounds or skew.
