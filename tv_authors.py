#painful data transformation
import pandas as pd
wiki_df = pd.read_csv('notmyrealfilepath')
authors = wiki_df.groupby(['Written by']).size()

author_season_groups = wiki_df.groupby(['Written by', 'Season']).size()
author_season_groups = author_season_groups.reset_index()

#find most_frequent
most_frequent_df = author_season_groups[author_season_groups['Written by'].isin(most_frequent)].copy()
less_frequent_df = author_season_groups[~author_season_groups['Written by'].isin(most_frequent)].copy()

most_frequent_df.columns = [u'Written by', u'Season', u'Number']

everyone_else_df = less_frequent_df.groupby('Season').sum()
everyone_else_df = everyone_else_df.reset_index()
everyone_else_df['Written by'] = 'Other'
everyone_else_df.columns = [u'Season', u'Number', u'Written by']
everyone_else_df = everyone_else_df[['Written by', 'Season', 'Number']]

final_df = pd.concat([most_frequent_df, everyone_else_df])
final_df.to_csv('summary_author.csv', index=False)


#####

repeats_df = wiki_df[[u'Directed by', u'No. in season', u'No. in series', u'Original air date', u'Production Code', u'Season', u'Title', u'U.S. viewers (million)']]
no_repeats_df = repeats_df.drop_duplicates()

directors = no_repeats_df.groupby(['Directed by']).size()
directors = directors.order(ascending=False)
#50
most_frequent = directors[0:9]
most_frequent = most_frequent.index.tolist()

director_season_groups = no_repeats_df.groupby(['Directed by', 'Season']).size()
director_season_groups = director_season_groups.reset_index()

most_frequent_df = director_season_groups[director_season_groups['Directed by'].isin(most_frequent)].copy()
less_frequent_df = director_season_groups[~director_season_groups['Directed by'].isin(most_frequent)].copy()

most_frequent_df.columns = [u'Directed by', u'Season', u'Number']

everyone_else_df = less_frequent_df.groupby('Season').sum()
everyone_else_df = everyone_else_df.reset_index()
everyone_else_df['Directed by'] = 'Other'
everyone_else_df.columns = [u'Season', u'Number', u'Directed by']
everyone_else_df = everyone_else_df[['Directed by', 'Season', 'Number']]

final_df = pd.concat([most_frequent_df, everyone_else_df])
final_df.to_csv('summary_director.csv', index=False)
