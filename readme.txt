LabelGen – Avery 5160 QR Label Generator  
Written by Jefferson Kline  
Written for: Vogel Plant Pathology - Dr. Wilson Craine & Team 


## Before running

This program generates print-ready Avery 5160 label PDFs from a formatted CSV file.  
Each label will display a QR code on the left and up to 5 short text lines on the right.

Make sure:
    1. You are on a Windows machine (preferred).
    2. You have a Labels.csv file ready in the proper format.
    3. Each label line (text) should be no more than 31 characters.


## How to run

1: Open a command prompt in the same folder as LabelGen.exe

2: Run the tool with:
       LabelGen.exe path_to_your_csv

   Example:
       LabelGen.exe "C:/Users/you/Desktop/Labels.csv"

3: Your QR-coded label PDF will be created in the same folder as LabelGen.exe


## CSV Format Guide

- Row 0: Column flags ("H" for human text, "Q" for QR only, "H/Q" for both)
- Row 1: Column names (e.g., Name, Species, Plot, Rep)
- Row 2 and below: Data rows

    Example:

        H,H,Q,H,Q
        Name,Species,Plot,Rep,Date
        Pennycress,Crop,14,B,5/25
        ...more rows

- At most 5 columns should be marked as "H" or "H/Q" to avoid overflowing the label

- All human-readable lines must be 31 characters or fewer


## Output

- AveryLabels.pdf will be saved next to the LabelGen.exe
- QR codes are generated temporarily and automatically deleted after use


## Trouble Shooting

2: Installing missing dependencies with command in console may fix issues mentioning missing imports or libraries:

    'pip install -r requirements.txt'

    NOTE: if this fails open requirements.txt and install each manually with:

        'pip install <DEPENDENCY>', do not include the version number with this: numpy>=1.24 would be 'pip install numpy'

