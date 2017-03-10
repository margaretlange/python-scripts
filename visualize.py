#functions for visualizing your data

def print_tag_cloud_text(tags, posts, data, countfilepath):
    counts = open(countfilepath, 'w')
    for index, tag in enumerate(tags):
        num_appearance = int(sum(data[index]))
        for i in range(num_appearance):
            phrase = '~'.join(tag.split(' '))
            counts.write(phrase + " ")
        counts.write("\n")
    counts.close()
    
    
