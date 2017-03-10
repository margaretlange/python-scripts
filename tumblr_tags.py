from datetime import datetime
import numpy as np
import pandas as pd
import json
import pytumblr
import nltk
import re
import os
from visualize import print_tag_cloud_text
#

#process_post should be a function

def sample_from_tag(client, tag, timestamps, process_post, *args):
    for index, timestamp in enumerate(timestamps):
        print "processing post " + str(index)
        posts = client.tagged(tag, limit=1, before=timestamp)
        try:
            post = posts[0]
        except IndexError:
            print "no post, I guess"
            continue
        try:
            process_post(post, *args)
        except KeyError:
            print "discarding this post"
            continue
    return timestamps
    
#expects start_date, end_date as %Y-%m-%d
#takes a bit of time
#I don't think this is a simple random sample, but what is it?
def get_unix_timestamps(start_date, end_date, num_stamps):
    start_dt = datetime.strptime(start_date,'%Y-%m-%d')
    start_timestamp = start_dt.strftime('%s')
    end_dt = datetime.strptime(end_date,'%Y-%m-%d')
    end_timestamp = end_dt.strftime('%s')
    ts_array = np.arange(int(start_timestamp), int(end_timestamp) + 1) 
    draw = np.random.choice(ts_array, num_stamps, replace=False)
    return draw
    
#redo this    
#don't exclude anything for the first try  
#this doesn't successfully exclude tags with spaces
#why are these 1s-get rid of
def process_tags(post, tag_dict, post_ids, to_exclude):
    chare=re.compile(r'[!-\.&]')
    post_tags = post['tags']
    #print len(post_tags)
    id = post['id']
    if id in post_ids:
        print "found a duplicate"
        return
    post_ids.append(id)
    for tag in post_tags:
        tag_lower =re.sub(chare,'',tag.lower()).strip()
        tag_cleaned = ' '.join([t for t in tag_lower.split(' ') if t not in to_exclude])
        if len(tag_cleaned)<2: continue
        tag_dict.setdefault(tag_cleaned,[])
        tag_dict[tag_cleaned].append(id)
    

def process_text(post, text_dict):
    pass

def get_timestamps(post, timestamps):
    ts = post['timestamp']
    timestamps.append(ts)

#Adapted from Programming Collective Intelligence    
#needs to be edited to discard repeated posts for tags that aren't that popular
def print_tag_file_threshold(filepath, tag_dict, posts, threshold):
    out = file(filepath, 'w')
    out.write('Tag')
    for post_id in posts: out.write('\t%d' % int(post_id))
    out.write('\n')             
    for tag, tag_post_id in tag_dict.items():
        if len(tag_post_id) > threshold:
            try:
                out.write(tag)
            except UnicodeEncodeError:
                continue
            for post_id in posts:
                if post_id in tag_post_id: out.write('\t1')
                else: out.write('\t0')
            out.write('\n')

def print_tag_file_size(filepath, tag_dict, posts, num_tags):
    out = file(filepath, 'w')
    out.write('Tag')
    for post_id in posts: out.write('\t%d' % int(post_id))
    out.write('\n')  
    printed = 0
    for tag, tag_post_id in sorted(tag_dict.iteritems(), key=lambda kvt: len(kvt[1]), reverse=True):
        if printed == num_tags:
            break
        try:
            out.write(tag)
        except UnicodeEncodeError:
            continue
        for post_id in posts:
            if post_id in tag_post_id: out.write('\t1')
            else: out.write('\t0')
        out.write('\n')
        printed = printed + 1


#from Collective Intelligence
def readfile(filename):
  lines=[line for line in file(filename)]  
  # First line is the column titles
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    # First column in each row is the rowname
    rownames.append(p[0])
    # The data for this row is the remainder of the row
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data

def print_tag_counts(tags, posts, data, countfilepath):
    counts_array = []
    for index, tag in enumerate(tags):
        num_appearance = int(sum(data[index]))
        counts_array.append(num_appearance)
    df = pd.DataFrame({'id': tags, 'count': counts_array})
    df_sorted = df.sort(['count'], ascending=False)
    df_sorted.to_csv(countfilepath, header=True, index=False)
    



def main():
    configfilepath = os.path.expanduser('~/Desktop/tumblr.json')
    tags_filepath = '~/Desktop/tumblr_tag_demo/demo_all.txt'
    tags_filepath_small = 'demo_small.txt'
    with open(configfilepath, 'r') as configfile:
        cfg = json.load(configfile)
    client = pytumblr.TumblrRestClient(cfg['consumer_key'], cfg['consumer_secret'], cfg['oauth_token'], cfg['oauth_secret']) 
    my_start_date = '2015-01-01'
    my_end_date = '2015-05-31'
    #test sampling function
    print "getting timestamps"
    my_timestamps = get_unix_timestamps(my_start_date, my_end_date, 500)
    my_tag_dict = {}
    my_post_ids = []
    print "sampling from tag"
    #note: depending on the tag, you may not get back 500 distinct posts
    sample_from_tag(client, 'clinton', my_timestamps, process_tags, my_tag_dict, my_post_ids, ['clinton'])
    #NOTE: edit this function to discard repeated posts for less popular tags
    print "you sampled " + str(len(my_post_ids)) + " tags"
    print "printing to files"
    print_tag_file_threshold(tags_filepath, my_tag_dict, my_post_ids, 0)
    print_tag_file_size(tags_filepath_small, my_tag_dict, my_post_ids, 15)
    print "printing counts"
    tags, posts, data = readfile(tags_filepath)
    print_tag_counts(tags, posts, data, 'tag_counts_all.csv')
    #print_tag_cloud_text(tags, posts, data, 'tag_cloud.txt')
     

if __name__=="__main__":
    main()   


    