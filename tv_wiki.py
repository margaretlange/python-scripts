#code to scrape the television wikipedia pages


from bs4 import BeautifulSoup
import re
import pandas as pd

def process_viewers_string(viewers_string, my_regex):
    viewers_re = re.compile(r'[0-9]+\.[0-9]+')
    result = viewers_re.search(viewers_string)
    without_citation = result.group()
    if without_citation is not None:
    	return without_citation
    else:
    	print "viewers string regex failed for " + viewers_string
    	return viewers_string

def process_date_string(date_string, my_regex):
	cleaned = date_string.replace(u'\xa0', u' ')
	result = my_regex.search(cleaned)
	try:
        final_date = result.group(3)	
        return final_date
	except:
        print "date string regex failed for " + date_string
        return date_string
		
def process_writer_string(writer_string, my_regex):
    episode_writers = []
    intermediate = get_story_teleplay(writer_string, my_regex)
    for elem in intermediate:
        check_multiple = elem.split('&')
        for author in check_multiple:
            episode_writers.append(author.strip())
    return list(set(episode_writers))

def get_story_teleplay(writer_string, my_regex):
    result = my_regex.search(writer_string)
    if result is None:
        return [writer_string]
    else:
        story_authors = result.group(2)
        teleplay_authors = result.group(5)
        return [story_authors, teleplay_authors]


season_file_path = 'not my real file path'
season_file = open(season_file_path, 'r')

soup = BeautifulSoup(season_file.read())
season_file.close()

season_array = []
number_series = []
number_season = []
title = []
director = []
writers = []
air_date = []
production_code = []
us_viewers_million = []



tables = soup.find_all('table')

story_teleplay_re = re.compile(r'(Story by: )([A-Za-z &.]*)(\n)(Teleplay by: )([A-Za-z &.]*)')
date_re = re.compile(r'([A-Za-z]+ [0-9]+, [0-9]+ )(\()([0-9]+-[0-9]+-[0-9]+)')
viewers_re = re.compile(r'[0-9]+\.[0-9]+')

for elem in range(10):
    season_num = elem + 1
    print "Season " + str(season_num)
    my_season = tables[season_num]
    rows = my_season.find_all('tr')
    num_episodes = len(rows)
    episodes = rows[1:num_episodes]
    for index, episode in enumerate(episodes):
        print "now on episode " + str(index)
        num_series = episode.find('th').get_text()
        columns = episode.find_all('td')
        episode_title = columns[1].get_text()
        episode_title = episode_title.replace('"', '')
        print episode_title
        date_string = columns[4].get_text()
        short_date = process_date_string(date_string, date_re)
        viewers_string = columns[6].get_text()
        short_viewers = process_viewers_string(viewers_string, viewers_re)
        code_string = columns[5].get_text()
        writer_string = columns[3].get_text()
        season_episode = columns[0].get_text()
        all_writers = process_writer_string(writer_string, story_teleplay_re)
        for writer in all_writers:
            season_array.append(season_num)
            number_series.append(num_series)
            number_season.append(season_episode)
            title.append(episode_title)
            director.append(columns[2].get_text())
            writers.append(writer)
            air_date.append(short_date)
            us_viewers_million.append(short_viewers)
            production_code.append(code_string)


test = pd.DataFrame({'Season': season_array, 'No. in series': number_series, 'No. in season': number_season, 'Title': title, 'Directed by': director, 'Written by': writers, 'Original air date': air_date, 'Production Code': production_code, 'U.S. viewers (million)': us_viewers_million})
test.to_csv('episodes.csv', index=False)

