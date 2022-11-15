from bs4 import BeautifulSoup
import requests
import csv

#Open CSV File
csv_file = open('cms_scrape_test.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['movie_genres'])

#Get the URL
url_list = requests.get('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres=action&start=1&explore=genres&ref_=adv_nxt').text
soup1= BeautifulSoup(url_list, 'lxml')

#Create the Movie List HTML
movie_item = soup1.find('div', class_='lister-item mode-advanced')

 #Find the Link to the Movie
movie_link = movie_item.find(class_='lister-item-image float-left').a['href']
url_movie = requests.get('https://www.imdb.com'+str(movie_link)).text

#Find the Genres of the Movie
movie_genres = movie_item.find('span', class_='genre').text

#Create Soup for the Movie Page
soup2 = BeautifulSoup(url_movie, 'lxml')
for x in range(1,13):
    print(x)
    movie_pictures_ref = soup2.find('a',attrs={'data-testid': f'photos-image-overlay-{x}'}, class_='ipc-lockup-overlay ipc-focusable')['href']
    soup4 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_pictures_ref).text, 'lxml')
    movie_picture_link_HQ = soup4.find('img')['src']
    # movie_picture_link_LQ= soup4.find('img')['srcset'].split(' ')[0]
    print(movie_picture_link_HQ)

try:
    csv_writer.writerow([movie_genres])
except Exception as e:
    pass