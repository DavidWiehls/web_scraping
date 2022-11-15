from bs4 import BeautifulSoup
import requests

#Get the URL
url_list = requests.get('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres=action&start=1&explore=genres&ref_=adv_nxt').text
soup1= BeautifulSoup(url_list, 'lxml')

#Create the Movie List HTML
movie_item = soup1.find('div', class_='lister-list')

#Find the Link to the Movie
movie_link = movie_item.find(class_='lister-item-image float-left').a['href']
url_movie = requests.get('https://www.imdb.com'+str(movie_link)).text

#Create Soup for the Movie Page
soup2 = BeautifulSoup(url_movie, 'lxml')

#Find the Movie Name
movie_name = soup2.find('h1', attrs={'data-testid': 'hero-title-block__title'}).text

#Find the Original Name
try:
    movie_name_original = soup2.find('div', attrs={'data-testid': 'hero-title-block__original-title'}).text
except Exception as e:
    movie_name_original = movie_name
    pass

#Find the release Year
movie_release = soup2.find('a', attrs={'href': str(movie_link)+'releaseinfo?ref_=tt_ov_rdat'}).text

#Find the Cover Reference Link and then Find the Cover Link in HQ and LQ 
movie_cover_ref = soup2.find('a', class_='ipc-lockup-overlay ipc-focusable')['href']
soup3 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_cover_ref).text, 'lxml')
movie_cover_link_HQ = soup3.find('img')['src']
movie_cover_link_LQ= soup3.find('img')['srcset'].split(' ')[0]


#Find the Picture Reference Link and then Find the Picture Link in HQ and LQ 
# Find All needed
movie_pictures_ref = soup2.find('a',attrs={'data-testid': 'photos-image-overlay-1'}, class_='ipc-lockup-overlay ipc-focusable')['href']
soup4 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_pictures_ref).text, 'lxml')
movie_picture_link_HQ = soup4.find('img')['src']
movie_picture_link_LQ= soup4.find('img')['srcset'].split(' ')[0]

# # movie_next_episode = soup2.find('div', attrs={'data-testid': 'tm-box-up-date'}) #does not work

# Find a short presentation of the movie
movie_presentation = soup2.find('span', attrs={'data-testid': 'plot-xl'}).text


print('https://www.imdb.com'+str(movie_link))
print(movie_name)
print(movie_name_original)
print(movie_release)
print(movie_cover_link_HQ)
print(movie_cover_link_LQ)
print(movie_picture_link_HQ)
print(movie_picture_link_LQ)
print(movie_presentation)