QR Code Generator - Stylish QR Code Generation Application


**Description**

This modern application allows you to generate QR codes from text or URLs with a sleek cyberpunk/neon interface. Key features:

    Stylish cyberpunk/neon design

    Glitch effects and animations

    Save QR codes as PNG images

    Fully offline operation (no internet required)

Features

    Generate QR codes from any text or URLs

    Automatic QR code scaling

    Save as PNG with transparent background

    Hover effects on buttons

    Animated background

Installation
Requirements

    Python 3.7+

    PyQt5

    qrcode library

Install dependencies
bash

pip install PyQt5 qrcode

Run the application
bash

python qrcodegenerator.py

Building EXE (for distribution)

    Install PyInstaller:

bash

pip install pyinstaller

    Build the executable:

bash

pyinstaller --onefile --windowed --icon=icon.ico qrcodegenerator.py

    The compiled EXE will be in the dist/ folder

Usage

    Enter text or URL in the input field

    Click "GENERATE"

    Click "SAVE" to export as PNG file

Technical Details
Technologies Used

    Python 3

    PyQt5 for GUI

    qrcode library for QR generation

    Animation effects using QPropertyAnimation

Code Structure

    GlitchEffect - Class for glitch-effect text

    ModernButton - Styled animated buttons

    QRGenerator - Main application class

        initUI - Interface initialization

        generate_qr - QR code generation

        save_qr - Save QR code to file

License

This project is licensed under the MIT License. You are free to use, modify and distribute the code.

For questions and suggestions, please contact the project author.
