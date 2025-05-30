import re
import json

def structure_text_data(raw_text: str) -> dict:
    """
    Structures raw OCR text by extracting key-value pairs based on predefined patterns.

    Args:
        raw_text (str): The multiline string of text extracted by OCR.

    Returns:
        dict: A dictionary representing the structured data.
    """
    structured_data = {}

    # Define simple regex patterns for common lab report fields.
    # Each key in the dictionary is the desired field name, and the value is a regex pattern.
    # The regex should capture the value part of the "Key: Value" pair.
    # These patterns generally assume the key and value are on the same line.
    # Add more patterns here or modify existing ones to suit different report formats.
    # Using re.IGNORECASE in re.search, so patterns don't need to handle case variations like "patient name:" vs "Patient Name:".
    patterns = {
        "Patient Name": r"Patient Name:\s*(.*)",
        "Patient ID": r"Patient ID:\s*(.*)",
        "Date of Birth": r"Date of Birth:\s*(.*)|DOB:\s*(.*)", # Allow "DOB:"
        "Report Date": r"Report Date:\s*(.*)|Collection Date:\s*(.*)", # Allow "Collection Date:"
        "Test ID": r"Test ID:\s*(.*)|Accession Number:\s*(.*)", # Allow "Accession Number:"
        "Test Name": r"Test Name:\s*(.*)|Procedure:\s*(.*)", # Allow "Procedure:"
        "Result": r"Result:\s*(.*)",
        "Reference Range": r"Reference Range:\s*(.*)",
        "Abnormal Flag": r"Flag:\s*([HLABN]*)", # Catches H, L, A, B, N flags
        # To add more fields, simply add a new entry to this 'patterns' dictionary:
        # "New Field Name": r"Regex for New Field:\s*(.*)",
    }

    lines = raw_text.splitlines()

    for line in lines:
        for key, pattern in patterns.items():
            match = re.search(pattern, line, re.IGNORECASE) # Ignore case for robustness
            if match:
                # If the pattern has OR conditions (like DOB), find which group matched
                value = next((g for g in match.groups() if g is not None), None)
                if value:
                    # Simple handling: last match wins if key is repeated.
                    # More advanced: structured_data.setdefault(key, []).append(value.strip())
                    structured_data[key] = value.strip()
                    # Optimization: Once a pattern matches on a line, we can break
                    # from the inner loop if we assume one key-value pair per line.
                    # However, some lines might have multiple, or pattern could be too greedy.
                    # For now, let it check all patterns.

    return structured_data

if __name__ == '__main__':
    sample_raw_text = """
    Lab Report - General Hospital
    ---------------------------------
    Patient Name: John Doe
    Patient ID: JD12345
    Date of Birth: 01/15/1980
    Report Date: 2023-10-26
    Accession Number: X98765A
    Test Name: Glucose Level
    Result: 105 mg/dL
    Reference Range: 70-99 mg/dL
    Flag: H
    Notes: Patient was fasting.

    Test Name: Hemoglobin A1c
    Result: 5.7 %
    Reference Range: <5.7 %
    Notes: Borderline.
    """

    print("Original Raw Text:")
    print("-------------------")
    print(sample_raw_text)
    print("-------------------\n")

    structured_info = structure_text_data(sample_raw_text)

    print("Structured Data (JSON):")
    print("-------------------")
    print(json.dumps(structured_info, indent=4))
    print("-------------------\n") # Added newline for better separation

    # Test with slightly different formatting and some keys on the same line
    sample_raw_text_2 = """
    Patient Name: Jane Smith DOB: 03/20/1992
    Collection Date: 2023-10-27 Test ID: Y12345B Procedure: Lipid Panel
    Result: Cholesterol 200 mg/dL Flag: N
    Comment: This is a test comment.
    """
    print("Original Raw Text 2 (testing robustness):")
    print("-------------------")
    print(sample_raw_text_2)
    print("-------------------\n")
    structured_info_2 = structure_text_data(sample_raw_text_2)
    print("Structured Data 2 (JSON):")
    print("-------------------")
    print(json.dumps(structured_info_2, indent=4))
    print("-------------------")
