from tumblr_tags import readfile
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform, jaccard
import numpy as np
import pandas as pd
import os  # for os.path.basename
import matplotlib.pyplot as plt

#adapted from Programming Collective Intelligence
def tag_overlap(v1,v2):
  c1,c2,shr=0,0,0
  for i in range(len(v1)):
    if v1[i]!=0: c1+=1 # in v1
    if v2[i]!=0: c2+=1 # in v2
    if v1[i]!=0 and v2[i]!=0: shr+=1 # in both
  return (c1, c2, shr)  


def write_tag_distances(filename, tags, distanceMatrix):
    tag_one = []
    tag_two = []
    distances = []
    squaredist = squareform(distanceMatrix)
    distance_file = open(filename, 'w')
    for i, tagi in enumerate(tags):
        for j, tagj in enumerate(tags):
            tag_one.append(tagi)
            tag_two.append(tagj)
            distances.append(str(squaredist[i, j]))
    my_df = pd.DataFrame({'source': tag_one, 'target': tag_two, 'weight': distances}, columns=['source', 'target', 'weight'])
    my_df_sorted = my_df.sort_index(by='weight')
    my_df_sorted.to_csv(filename, index=False, header=True)
    
  
def main():
    tags, posts, data = readfile('~/Desktop/tumblr_tag_demo/demo_small.txt')
    dataMatrix = np.array(data) 
    my_distance_matrix = pdist(dataMatrix, 'jaccard')
    write_tag_distances('distances.csv', tags, my_distance_matrix)
    my_cluster = linkage(my_distance_matrix, method='weighted', metric='jaccard')
    fig, ax = plt.subplots(figsize=(30, 30)) # set size
    ax = dendrogram(my_cluster, orientation="top", labels=tags, show_leaf_counts=True)
    plt.tick_params(
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off')
    #plt.tight_layout() #show plot with tight layout
    #uncomment below to save figure
    plt.xticks(rotation=90, fontsize = 30)
    plt.yticks(fontsize=30)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('~/Desktop/tumblr_tag_demo/small_dendo.png', dpi=200)

if __name__=="__main__":
    main()  