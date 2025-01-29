# QR Code Generator Script

This script allows users to generate customizable QR codes with various options. It provides flexibility in personalizing the appearance of the QR code and offers multiple features to enhance the user experience. Below is a structured breakdown of the functionalities:

## Features

1. **URL or Custom Text Input:**
   - The user can input a URL or custom text to generate a QR code.
   - The script verifies if the URL is reachable before proceeding.

2. **File Name and Save Path:**
   - The user specifies the filename for the saved QR code image (without extension).
   - The script allows choosing the default save path or a custom directory for saving the image.

3. **Color Customization:**
   - The user can customize the fill (foreground) and background colors of the QR code.
   - It supports a range of colors, including named colors, hex codes, and RGB tuples.

4. **Box Size Customization:**
   - The user can specify the size of the individual boxes in the QR code.

5. **Logo Placement (Optional):**
   - The user can choose to add a logo to the center of the QR code.
   - The logo image is resized and pasted with proper transparency handling.

6. **Image Format Selection:**
   - The script allows the user to choose the format for the saved QR code image (e.g., PNG, JPEG, etc.).
   - It validates the format to ensure it's supported.

7. **QR Code Generation and Saving:**
   - The script generates the QR code based on the provided data and user preferences.
   - The QR code image is saved to the specified path in the chosen format.

8. **Preview Option (Optional):**
   - After saving the QR code, the user can choose to preview the image before finishing.
   - The image is displayed for review before exiting the script.

9. **Input Validation:**
   - The script checks the validity of the URL, image format, color input, and other user inputs to ensure correct data is provided.

This structure provides users with a fully customizable QR code generation experience, with options for personalizing colors, adding logos, and selecting file formats.

## License
This project is licensed under the MIT License --->  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)