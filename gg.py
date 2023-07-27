import os
from bs4 import BeautifulSoup
import csv

# Configuration: Set the desired delimiter
DELIMITER = "|"

# Function to extract data from the local HTML file
def extract_data_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Extracting required data from the HTML page
        title = soup.find('h1', class_='large-title')
        title_text = title.text.strip() if title else "N/A"

        publisher = soup.select_one('strong:contains("Publisher:") + a')
        publisher_text = publisher.text.strip() if publisher else "N/A"
        publisher_link = publisher.get('href') if publisher else "N/A"

        developer = soup.select_one('strong:contains("Developer:") + a')
        developer_text = developer.text.strip() if developer else "N/A"
        developer_link = developer.get('href') if developer else "N/A"

        price = soup.select_one('.js-price-line')
        price_text = price.text.strip() if price else "N/A"
        price_text = price_text.replace('\n', '').replace('\r', '').strip()

        genres = [genre.text.strip() for genre in soup.select('section:has(.section-title:contains("Genre")) a')]
        tags = [tag.text.strip() for tag in soup.select('section:has(.section-title:contains("Tags")) a')]

        languages = soup.select_one('span:contains("Languages:")')
        languages_text = languages.find_next('a').text.strip() if languages else "N/A"

        size = soup.select_one('span:contains("Download Size:")')
        size_text = size.find_next('span').text.strip() if size else "N/A"

        summary = soup.select_one('span:contains("Summary:")')
        summary_text = summary.find_next('span').text.strip() if summary else "N/A"

        key_features = soup.select_one('span:contains("Key features:")')
        key_features_text = key_features.find_next('span').text.strip() if key_features else "N/A"

        # Extracting files links
        files_links = [a.get('href') for a in soup.select('.p-files-link')]

        # Return the extracted data as a dictionary
        return {
            'Title Text': title_text,
            'Publisher Text': publisher_text,
            'Publisher Link': publisher_link,
            'Developer Text': developer_text,
            'Link to Developer': developer_link,
            'Price': price_text,
            'Genre': ','.join(genres),
            'Tags': ','.join(tags),
            'Languages': languages_text,
            'Size text': size_text,
            'Summary': summary_text,
            'Key features': key_features_text,
            'Files': ','.join(files_links),
        }

    except Exception as e:
        print(f"Error processing file: {file_path}\nError: {e}")
        return None

# Function to export data to a CSV file
def export_to_csv(data_list, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        if not data_list:  # Check if the data_list is empty
            print("No data to export.")
            return

        # Use the custom delimiter when initializing the CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys(), delimiter=DELIMITER)

        writer.writeheader()
        for data in data_list:
            # Remove any extra whitespace and line breaks from the values
            for key in data:
                data[key] = data[key].replace('\n', '').replace('\r', '').strip()
            writer.writerow(data)

if __name__ == "__main__":
    # Set the path to the directory containing the HTML files
    html_files_directory = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\datafiles"

    # Get a list of all HTML files in the directory
    html_files = [os.path.join(html_files_directory, file) for file in os.listdir(html_files_directory) if file.endswith('.html')]

    # Extract data from each HTML file and store in a list of dictionaries
    extracted_data = []
    for file_path in html_files:
        data = extract_data_from_file(file_path)
        if data:
            extracted_data.append(data)

    # Export data to CSV file
    export_to_csv(extracted_data, 'articles_data.csv')

    print("Data extraction and CSV export completed successfully.")