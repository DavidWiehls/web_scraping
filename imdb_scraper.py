from bs4 import BeautifulSoup
import requests
import csv

#Open CSV File
csv_file = open('cms_scrape.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow([   'movie_name',
                        'movie_name_original',
                        'movie_genres',
                        'movie_release',
                        'movie_cover_link_HQ',
                        'movie_cover_link_LQ',
                        'movie_presentation'
                        'movie_stars'
                                                ])


# for x in range(1,9952):
#Get the URL
url_list = requests.get('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres=action&start=1&explore=genres&ref_=adv_nxt').text
soup1= BeautifulSoup(url_list, 'lxml')

#Create the Movie List HTML
for movie_item in soup1.find_all('div', class_='lister-item mode-advanced'):

    #Find the Link to the Movie
    movie_link = movie_item.find(class_='lister-item-image float-left').a['href']
    url_movie = requests.get('https://www.imdb.com'+str(movie_link)).text

    #Find the Genres of the Movie
    movie_genres = movie_item.find('span', class_='genre').text.split('\n')[1].rstrip()

    #Create Soup for the Movie Page
    soup2 = BeautifulSoup(url_movie, 'lxml')

    #Find the Movie Name
    movie_name = soup2.find('h1', attrs={'data-testid': 'hero-title-block__title'}).text

    #Find the Original Name
    try:
        movie_name_original = soup2.find('div', attrs={'data-testid': 'hero-title-block__original-title'}).text.strip('Originaltitle: ')
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


    # #Find the Picture Reference Link and then Find the Picture Link in HQ and LQ 
    # # Find All needed
    # for x in range(1,13):
    #     csv_file = open('cms_scrape_pictures.csv', 'w', newline='')
    #     csv_writer = csv.writer(csv_file)
    #     csv_writer.writerow(['movie_name', 'movie_name_original', 'movie_picture_link_HQ_1', 'movie_picture_link_HQ_12' ])

    #     movie_pictures_ref = soup2.find('a',attrs={'data-testid': f'photos-image-overlay-{x}'}, class_='ipc-lockup-overlay ipc-focusable')['href']
    #     soup4 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_pictures_ref).text, 'lxml')
    #     movie_picture_link_HQ = soup4.find('img')['src']
    #     # movie_picture_link_LQ= soup4.find('img')['srcset'].split(' ')[0]
    # try:
    #     csv_writer.writerow([])
    # except Exception as e:
    #     print('ERROR in ' + str(movie_name))
    #     pass

    # # movie_next_episode = soup2.find('div', attrs={'data-testid': 'tm-box-up-date'}) #does not work

    # Find a short presentation of the movie
    movie_presentation = soup2.find('span', attrs={'data-testid': 'plot-xl'}).text 
    # or also in soup1
    # movie_presentation = movie_item.find(class_='text-muted').find_next(class_='text-muted').find_next(class_='text-muted').text

    # Find the main artists in the movie
    movie_stars_row = movie_item.find(class_='text-muted').find_next(class_='text-muted').find_next(class_='text-muted').find_next().text
    movie_stars_list = movie_stars_row.split(':')[1].split('\n')
    movie_stars = "".join(movie_stars_list)


    # print('https://www.imdb.com'+str(movie_link))
    # print(movie_name)
    # print(movie_name_original)
    # print(movie_genres)
    # print(movie_release)
    # print(movie_cover_link_HQ)
    # print(movie_cover_link_LQ)
    # print(movie_presentation)
    # print(movie_stars)

    try:
        csv_writer.writerow([   movie_name,
                                movie_name_original,
                                movie_genres,
                                movie_release,
                                movie_cover_link_HQ,
                                movie_cover_link_LQ,
                                movie_presentation,
                                movie_stars
                                                        ])
    except Exception as e:
        print('ERROR in ' + str(movie_name))
        pass
    print(movie_name+' is done')

csv_file.close()