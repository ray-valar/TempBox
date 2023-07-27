import os
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_links_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'html.parser')

            # Find the <section> element with class "flx-column product-gallery"
            product_gallery_section = soup.find('section', class_='flx-column product-gallery')

            if product_gallery_section:
                # Find all the <a> tags within the product_gallery_section
                a_tags = product_gallery_section.find_all('a')

                # Extract the href attribute from each <a> tag and store them in a list
                links = [a_tag.get('href') for a_tag in a_tags]

                # Find the first <video> element within the product_gallery_section
                video_tag = product_gallery_section.find('video')

                # Extract the source attribute from the video_tag if it exists
                if video_tag:
                    video_link = video_tag.source.get('src')
                    links.insert(0, video_link)

                # Remove query parameters from the links
                links = [urlparse(link)._replace(query='').geturl() for link in links]

                return links

            else:
                print(f"Product gallery section not found in file: {file_path}")
                return []

    except Exception as e:
        print("Error:", e)
        return []


if __name__ == "__main__":
    folder_path = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\datafiles"
    output_csv_path = r"C:\Users\PC-Admin\Downloads\OA New\PS\new\links_output.csv"

    # List all the files in the datafiles directory
    file_list = os.listdir(folder_path)

    # Initialize a dictionary to store the links for each file
    links_data = {}

    # Process each file to extract the links
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        links = extract_links_from_file(file_path)
        links_data[file_name] = links

    # Export the links data to a CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['File', 'Links'])
        for file_name, links in links_data.items():
            csv_writer.writerow([file_name] + links)

    print("Links data exported to CSV successfully.")
