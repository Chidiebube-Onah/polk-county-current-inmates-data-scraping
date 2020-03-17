import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import sys
import time


# Set headers

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
url = "https://apps.polkcountyiowa.gov/PolkCountyInmates/CurrentInmates/Details?Book_ID=310750"

# req = requests.get(url, headers)
# soup = BeautifulSoup(req.content, 'html.parser')
# print(soup.prettify())


def get_img_url(url):

    try:
        req = requests.get(url, headers)
    except requests.exceptions.ConnectionError as e:
        sys.exit(f"An Error Ocuured...Check Internet Connection\n{e}")
    else:
        soup = BeautifulSoup(req.content, 'html.parser')
        details = soup.find('div', class_ = 'row')
        # img scr
        temp_img_src = details.div.img.attrs.get('src')
        img_src = "https://" + url.split("/")[2] + temp_img_src

        return img_src

def info(url=url):

    try:
        req = requests.get(url, headers)
    except requests.exceptions.ConnectionError as e:
        sys.exit(f"An Error Ocuured...Check Internet Connection\n{e}")
    else:
        soup = BeautifulSoup(req.content, 'html.parser')
        details = soup.find('div', class_ = 'row')
    
        return details.find('div', class_ = 'col-md-9')

def get_info(data):

    data_value = data.next_sibling.strip()
    return data_value

def datarow(url=url):

    Info = info(url)

    label = Info.find(attrs={'for': "Offender_Name_ID:_"})
    name = Info.find(attrs={'for': "Name:_"})
    book = Info.find(attrs={'for': "Book_Date:_"})
    city = Info.find(attrs={'for': "City:_"})
    HL = Info.find(attrs={'for': "Holding_Location:_"})
    age = Info.find(attrs={'for': "Age:_"})
    height = Info.find(attrs={'for': "Height:_"})
    weight = Info.find(attrs={'for': "Weight:_"})
    race = Info.find(attrs={'for': "Race:_"})
    eyes = Info.find(attrs={'for': "Eyes:_"})
    hair = Info.find(attrs={'for': "Hair:_"})
    sex = Info.find(attrs={'for': "Sex:_"})
    img_scr =  "images/" + get_info(label) + ".jpg"
   
    return [
            get_info(label),
            get_info(name),
            get_info(book),
            get_info(city),
            get_info(HL),
            get_info(age),
            get_info(height),
            get_info(weight),
            get_info(race),
            get_info(sex),
            get_info(eyes),
            get_info(hair),
            img_scr

            ]


def download(url, pathname="images"):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    buffer_size = 1024
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    try:
        # download the body of response by chunk, not immediately
        response = requests.get(url, stream=True)
    except requests.exceptions.ConnectionError as e:
        sys.exit(f"An Error occured!!!...Check your Internet Connection!!!\n{e}")
    else:
        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        # get the file name
        filename = os.path.join(pathname, url.split("=")[-1])
        filename += ".jpg"
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))
                

