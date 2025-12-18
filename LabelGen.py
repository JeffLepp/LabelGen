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

#   Alerts users:
#   - Replace Excel and QR example w/ H/Q 
#

def is_blank(col):
    return col.iloc[2:].apply(lambda x: str(x).strip() == "").all()

def clean(s):
    if not isinstance(s, str):
        s = str(s)
    return s.replace("\n", "_").replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").strip()


def main(csv_path):
# Read file (change suffix to '.xlsx' if needed)
    path = Path(csv_path).resolve()

    # Here are some general checks for input given
    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist.")

    if path.suffix.lower() == ".csv":
        df_raw = pd.read_csv(path, header=None, keep_default_na=False)
    elif path.suffix.lower() in (".xls", ".xlsx"):
        df_raw = pd.read_excel(path, header=None)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv file.")

    df_raw = df_raw.loc[:, ~df_raw.apply(is_blank, axis=0)]

    # Extract header metadata
    excel_flags = df_raw.iloc[0]   # Row of H/Q
    excel_headers = df_raw.iloc[1] # Row of actual excel_headers
    excel_data = df_raw.iloc[2:].reset_index(drop=True)

    # Making map of normalized flags
    valid_flags = {"H", "Q", "H/Q"}
    flag_map = {
        col: flag.strip().upper()
        for col, flag in zip(excel_headers, excel_flags)
        if col.strip() != "" and flag.strip().upper() in valid_flags
    }

    flag_tuples = [
        (i, col, flag.strip().upper())
        for i, (col, flag) in enumerate(zip(excel_headers, excel_flags))
        if str(col).strip() != "" and flag.strip().upper() in valid_flags
    ]

    # Correct duplicate check logic for overlaps:
    h_fields = [col for col, flag in flag_map.items() if flag == "H"]
    hq_fields = [col for col, flag in flag_map.items() if flag == "H/Q"]
    q_fields = [col for col, flag in flag_map.items() if flag == "Q"]

    hq_overlap_with_h = set(hq_fields).intersection(h_fields)
    hq_overlap_with_q = set(hq_fields).intersection(q_fields)

    if hq_overlap_with_h:
        raise ValueError(f"Columns duplicated in both H and H/Q: {', '.join(hq_overlap_with_h)}")
    if hq_overlap_with_q:
        raise ValueError(f"Columns duplicated in both Q and H/Q: {', '.join(hq_overlap_with_q)}")

    if len(excel_headers) != len(excel_flags):
        raise ValueError("Mismatch between number of column headers and flag entries.")
    
    if "" in excel_headers.values:
        raise ValueError("There is a mismatch between number of H,Q,H/Q or headers compared to number of columns.")
    
    if sum(flag in ("H", "H/Q") for flag in excel_flags) > 5:
        raise ValueError("Exceeded 5 lines of text between H and H/Q columns.")

    valid_flags = {"H", "Q", "H/Q"}

    if not all(flag in valid_flags for flag in excel_flags):
        raise ValueError("Invalid column flag. Only 'H', 'Q', or 'H/Q' allowed.")

    excel_data.columns = excel_headers  # Rename columns using actual excel_headers
    excel_flags.index = excel_headers   # Align excel_flags to excel_headers

    # Split fields (what will be on label vs QR or both!)
    human_cols = [col for i, col, flag in flag_tuples if flag in ("H", "H/Q")]
    qr_cols    = [col for i, col, flag in flag_tuples if flag in ("Q", "H/Q")]

    print(f"Human columns: {human_cols}")
    print(f"QR columns: {qr_cols}")
    labels_to_paste = []
    temp_qr_files = []


    for idx, row in excel_data.iterrows():
        # Text for human-readable label (limit to 5 lines later if needed)
        label_lines = []
        for col in human_cols:
            val = row[col]
            # Handle edge case where row[col] is a Series (multi-indexed df)
            if isinstance(val, pd.Series):
                val = val.iloc[0]
            label_lines.append(f"{col}: {str(val).strip()}")
        
        # Build QR string — here, simple braced format
        qr_string = "".join(
            "{" + col + "_" + (str(row[col].values[0]).strip() if isinstance(row[col], pd.Series) else str(row[col]).strip()) + "}"
            for col in qr_cols
        )      

        qr_string = "'" + qr_string + "'"

        filename_suffix = f"Label_{idx + 1}"
        qr_filename = f"QR_Label_{idx + 1}.png"
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
    print("Welcome to LabelGen!")

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