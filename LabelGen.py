import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources") #pyinstaller pkg_resources UserWarning fix, they will remove it at the end of 2025, no impact here
import pandas as pd
from pathlib import Path
from MakeQR import start
from LabelPaste import insert_labels_pdf
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import time

def main(csv_path):
# Read file (change suffix to '.xlsx' if needed)
    path = Path(csv_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist.")

    if path.suffix.lower() == ".csv":
        df_raw = pd.read_csv(path, header=None, keep_default_na=False)
    elif path.suffix.lower() in (".xls", ".xlsx"):
        df_raw = pd.read_excel(path, header=None)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv file.")

    # Extract header metadata
    excel_flags = df_raw.iloc[0]   # Row of H/Q
    excel_headers = df_raw.iloc[1] # Row of actual excel_headers
    excel_data = df_raw.iloc[2:].reset_index(drop=True)


    excel_data.columns = excel_headers  # Rename columns using actual excel_headers
    excel_flags.index = excel_headers   # Align excel_flags to excel_headers

    # Split fields
    human_cols = [col for col in excel_headers if excel_flags[col] == "H"]
    qr_cols    = [col for col in excel_headers if excel_flags[col] in ("H", "Q")]

    print(f"Human columns: {human_cols}")
    print(f"QR columns: {qr_cols}")
    labels_to_paste = []
    temp_qr_files = []


    for idx, row in excel_data.iterrows():
        # Text for human-readable label (limit to 5 lines later if needed)
        label_lines = [str(row[col]) for col in human_cols]
        
        # Build QR string — here, simple braced format
        qr_string = "".join("{" + str(row[col]) + "}" for col in qr_cols)
        
        # Make filename safe and unique using, e.g., Plot and Rep
        plot = str(row.get("Plot", f"Row{idx}"))
        rep = str(row.get("Rep", f"X"))
        filename_suffix = f"{plot}_{rep}".replace(" ", "_")
        qr_filename = f"QR_{filename_suffix}.png"
        temp_qr_files.append(qr_filename)

        # Call MakeQR generator
        start(qr_string, filename_suffix)
        labels_to_paste.append((qr_filename, label_lines))

        # For now, just print (replace this with QR/image/Word generation later)
        print(f"\n--- Label {idx + 1} ---")
        print("Label lines:")
        for line in label_lines:
            print("  ", line)
        print("QR string:", qr_string)

    insert_labels_pdf(qr_folder=".", labels=labels_to_paste)

    # Clean up QR codes
    for file in temp_qr_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Warning: Failed to delete {file}: {e}")

def get_excel_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls *.csv")]
    )
    return file_path


if __name__ == "__main__":
    print("Welcome to LabelGen! Contact jefferson.kline@wsu.edu for assistance or code requests for your lab (free).")

    try:
        if len(sys.argv) >= 2:
            main(sys.argv[1])
        else:
            chosen_file = get_excel_file()
            if chosen_file:
                main(chosen_file)
            else:
                messagebox.showinfo("LabelGen", "No file selected. Exiting.")
    except Exception as e:
        messagebox.showerror("LabelGen Error", str(e))
        sys.exit(1)
