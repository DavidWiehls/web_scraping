from bs4 import BeautifulSoup
import requests
import csv

#Open CSV File Movie Details
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

#Open CSV File Movie Picture 
# csv_file_pictures = open('cms_scrape_pictures.csv', 'w', newline='')
# csv_writer = csv.writer(csv_file_pictures)
# csv_writer.writerow([   'movie_name',
#                         'picture_1_HQ',
#                         'picture_2_HQ',
#                         'picture_3_HQ',
#                         'picture_4_HQ',
#                         'picture_5_HQ',
#                         'picture_6_HQ',
#                         'picture_7_HQ',
#                         'picture_8_HQ',
#                         'picture_9_HQ',
#                         'picture_10_HQ',
#                         'picture_11_HQ',
#                         'picture_12_HQ',
#                         'picture_1_LQ',
#                         'picture_2_LQ',
#                         'picture_3_LQ',
#                         'picture_4_LQ',
#                         'picture_5_LQ',
#                         'picture_6_LQ',
#                         'picture_7_LQ',
#                         'picture_8_LQ',
#                         'picture_9_LQ',
#                         'picture_10_LQ',
#                         'picture_11_LQ',
#                         'picture_12_LQ',

#                                                 ])

# for x in range(1,9952):
#Get the URL
url_list = requests.get('https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres=action&start=9951&explore=genres&ref_=adv_nxt').text
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
    try:
        movie_release = soup2.find('a', attrs={'href': str(movie_link)+'releaseinfo?ref_=tt_ov_rdat'}).text
    except Exception as e:
        movie_release = 'unknown'
        pass

    #Find the Cover Reference Link and then Find the Cover Link in HQ and LQ 
    try:
        movie_cover_ref = soup2.find('a', class_='ipc-lockup-overlay ipc-focusable')['href']
        soup3 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_cover_ref).text, 'lxml')
        movie_cover_link_HQ = soup3.find('img')['src']
        movie_cover_link_LQ= soup3.find('img')['srcset'].split(' ')[0]
    except Exception as e:
        movie_cover_link_HQ = 'no cover'
        movie_cover_link_LQ = 'no cover'
        pass


    # #Find the Picture Reference Link and then Find the Picture Link in HQ and LQ 
    # movie_picture_link_HQ = [None]*12
    # movie_picture_link_LQ = [None]*12

    # for x in range(1,13):
    #     movie_pictures_ref = soup2.find('a',attrs={'data-testid': f'photos-image-overlay-{x}'}, class_='ipc-lockup-overlay ipc-focusable')['href']
    #     soup4 = BeautifulSoup(requests.get('https://www.imdb.com'+movie_pictures_ref).text, 'lxml')
    #     movie_picture_link_HQ[x-1] = soup4.find('img')['src']
    #     movie_picture_link_LQ[x-1]= soup4.find('img')['srcset'].split(' ')[0]
    # try:
    #     csv_writer.writerow([   movie_name,
    #                             movie_picture_link_HQ[0],
    #                             movie_picture_link_HQ[1],
    #                             movie_picture_link_HQ[2],
    #                             movie_picture_link_HQ[3],
    #                             movie_picture_link_HQ[4],
    #                             movie_picture_link_HQ[5],
    #                             movie_picture_link_HQ[6],
    #                             movie_picture_link_HQ[7],
    #                             movie_picture_link_HQ[8],
    #                             movie_picture_link_HQ[9],
    #                             movie_picture_link_HQ[10],
    #                             movie_picture_link_HQ[11],
    #                             movie_picture_link_LQ[0],
    #                             movie_picture_link_LQ[1],
    #                             movie_picture_link_LQ[2],
    #                             movie_picture_link_LQ[3],
    #                             movie_picture_link_LQ[4],
    #                             movie_picture_link_LQ[5],
    #                             movie_picture_link_LQ[6],
    #                             movie_picture_link_LQ[7],
    #                             movie_picture_link_LQ[8],
    #                             movie_picture_link_LQ[9],
    #                             movie_picture_link_LQ[10],
    #                             movie_picture_link_LQ[11],
    #                                                     ])
    # except Exception as e:
    #     pass

    # # movie_next_episode = soup2.find('div', attrs={'data-testid': 'tm-box-up-date'}) #does not work

    # Find a short presentation of the movie
    try:
        movie_presentation = soup2.find('span', attrs={'data-testid': 'plot-xl'}).text 
    except Exception as e:
        movie_presentation = 'no presentation'
        pass
    # or also in soup1
    # movie_presentation = movie_item.find(class_='text-muted').find_next(class_='text-muted').find_next(class_='text-muted').text

    # Find the main artists in the movie
    try:
        movie_stars_row = movie_item.find(class_='text-muted').find_next(class_='text-muted').find_next(class_='text-muted').find_next().text
        movie_stars_list = movie_stars_row.split(':')[1].split('\n')
        movie_stars = "".join(movie_stars_list)
    except Exception as e:
        movie_stars = 'unknown'
        pass

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
# csv_file_pictures.close()