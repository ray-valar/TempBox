import os
import csv
from bs4 import BeautifulSoup

def extract_key_features_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Find the index of "●" symbol in the content
            key_features_index = content.find("●")

            if key_features_index != -1:
                # Extract everything following "●" symbol
                key_features_text = content[key_features_index:].strip()

                # Find the index of the first closing </div> tag after "●" symbol
                closing_div_index = key_features_text.find("</div>")

                if closing_div_index != -1:
                    # Extract the content until the first closing </div> tag
                    key_features_text = key_features_text[:closing_div_index].strip()

                    # Remove "●" symbols and replace line breaks with commas
                    key_features_text = key_features_text.replace("●", "").replace("<br/>", ", ").strip()

                    # Remove leftover tags and clean up entries
                    soup = BeautifulSoup(key_features_text, 'html.parser')
                    cleaned_text = [entry.strip() for entry in soup.get_text().splitlines() if entry.strip()]

                    return ", ".join(cleaned_text)

            print(f"Key Features section not found in file: {file_path}")
            return "N/A"

    except Exception as e:
        print("Error:", e)
        return "N/A"

if __name__ == "__main__":
    folder_path = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\datafiles"
    output_csv_path = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\output_key_features_formatted.csv"

    # List all the files in the folder
    file_list = os.listdir(folder_path)

    # Initialize a list to store the key features data
    key_features_data = []

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        key_features = extract_key_features_from_file(file_path)
        print(f"File: {file_name}")
        key_features_data.append((file_name, key_features))

    # Export the key features data along with formatted text to a CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File', 'Formatted Key Features'])
        csv_writer.writerows(key_features_data)

    print("Formatted Key Features data exported to CSV successfully.")
