from bs4 import BeautifulSoup
import requests
import csv

#Open CSV File
csv_file_pictures = open('cms_scrape_pictures_test.csv', 'w', newline='')
csv_writer = csv.writer(csv_file_pictures)
csv_writer.writerow([   'picture_1_HQ',
                        'picture_2_HQ',
                        'picture_3_HQ',
                        'picture_4_HQ',
                        'picture_5_HQ',
                        'picture_6_HQ',
                        'picture_7_HQ',
                        'picture_8_HQ',
                        'picture_9_HQ',
                        'picture_10_HQ',
                        'picture_11_HQ',
                        'picture_12_HQ',
                        'picture_1_LQ',
                        'picture_2_LQ',
                        'picture_3_LQ',
                        'picture_4_LQ',
                        'picture_5_LQ',
                        'picture_6_LQ',
                        'picture_7_LQ',
                        'picture_8_LQ',
                        'picture_9_LQ',
                        'picture_10_LQ',
                        'picture_11_LQ',
                        'picture_12_LQ',

                                                ])


#Get the URL
url_list = requests.get('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres=action&start=101&explore=genres&ref_=adv_nxt').text
soup1= BeautifulSoup(url_list, 'lxml')

#Create the Movie List HTML
movie_item = soup1.find('div', class_='lister-item mode-advanced')

#Find the Link to the Movie
movie_link = movie_item.find(class_='lister-item-image float-left').a['href']
url_movie = requests.get('https://www.imdb.com'+str(movie_link)).text

#Create Soup for the Movie Page
soup2 = BeautifulSoup(url_movie, 'lxml')


# #Find the Picture Reference Link and then Find the Picture Link in HQ and LQ 

movie_picture_link_HQ = [None]*12
movie_picture_link_LQ = [None]*12

for x in range(1,13):
    movie_pictures_ref = soup2.find('a',attrs={'data-testid': f'photos-image-overlay-{x}'}, class_='ipc-lockup-overlay ipc-focusable')['href']
    soup4 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_pictures_ref).text, 'lxml')
    movie_picture_link_HQ[x-1] = soup4.find('img')['src']
    movie_picture_link_LQ[x-1]= soup4.find('img')['srcset'].split(' ')[0]
    print(movie_picture_link_HQ[x-1])
    print(movie_picture_link_LQ[x-1])
try:
    csv_writer.writerow([   movie_picture_link_HQ[0],
                            movie_picture_link_HQ[1],
                            movie_picture_link_HQ[2],
                            movie_picture_link_HQ[3],
                            movie_picture_link_HQ[4],
                            movie_picture_link_HQ[5],
                            movie_picture_link_HQ[6],
                            movie_picture_link_HQ[7],
                            movie_picture_link_HQ[8],
                            movie_picture_link_HQ[9],
                            movie_picture_link_HQ[10],
                            movie_picture_link_HQ[11],
                            movie_picture_link_LQ[0],
                            movie_picture_link_LQ[1],
                            movie_picture_link_LQ[2],
                            movie_picture_link_LQ[3],
                            movie_picture_link_LQ[4],
                            movie_picture_link_LQ[5],
                            movie_picture_link_LQ[6],
                            movie_picture_link_LQ[7],
                            movie_picture_link_LQ[8],
                            movie_picture_link_LQ[9],
                            movie_picture_link_LQ[10],
                            movie_picture_link_LQ[11],
                                                       ])
except Exception as e:
    pass

csv_file_pictures.close()