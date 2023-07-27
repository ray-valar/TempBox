import os
import csv
from bs4 import BeautifulSoup

def extract_summary_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Find the section with class "flx-column article-wysiwyg" containing the summary
            summary_section = soup.find(lambda tag: tag.name == 'section' and 'flx-column' in tag.get('class', []) and 'article-wysiwyg' in tag.get('class', []) and 'summary' in tag.get_text().lower())

            if summary_section:
                # Get the summary text from the section and remove HTML tags
                summary_text = ''.join(summary_section.stripped_strings)

                # Remove "Read More" if present
                summary_text = summary_text.replace("Read More", "").strip()

                # Remove "Summary of Game" if present
                summary_text = summary_text.replace("Summary of Game", "").strip()

                return summary_text
            else:
                print(f"Summary section not found in file: {file_path}")
                return "N/A"

    except Exception as e:
        print("Error:", e)
        return "N/A"


if __name__ == "__main__":
    folder_path = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\datafiles"
    output_csv_path = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\summary_output.csv"

    # List all the files in the datafiles directory
    file_list = os.listdir(folder_path)

    # Initialize a list to store the summary data
    summary_data = []

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        summary = extract_summary_from_file(file_path)
        print(f"File: {file_name} | Summary: {summary}")
        summary_data.append((file_name, summary))

    # Export the summary data to a CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File', 'Summary'])
        csv_writer.writerows(summary_data)

    print("Summary data exported to CSV successfully.")