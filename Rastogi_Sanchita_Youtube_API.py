
# Author:  Sanchita Rastogi
# ID: 10439951
# Subject: Online Social Networks

#  youtube_data.py searches YouTube for videos matching a search term
#  It writes info for each video, up to a specified maximum number, to a .csv file

# to run from terminal window:  
#      python3 youtube_data.py --search_term mysearch --search_max mymaxresults
#  where:  search_term = the term you want to search for;  default = music
#     and  search_max = the maximum number of results;  default = 30



#   I used --search_term as "friends" and search_max = 50
#   I am calculating the Mininmum and Maximum values for Views, Likes, Dislikes column
#   and also calculating the sum of the whole column

from apiclient.discovery import build      # use build function to create a service object

import argparse    #  need for parsing the arguments in the command line
import csv         #  need since search results will be contained in a .csv file
import unidecode   #  need for processing text fields in the search results
import pandas as pd # need for read, manipulation and analysis 
import numpy as np  # need for mathematical function

# put your API key into the API_KEY field below, in quotes
API_KEY = ""

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

#  function youtube_search retrieves the YouTube records

def youtube_search(options):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(q=options.search_term, part="id,snippet", maxResults=options.search_max).execute()
    
    # create a CSV output for results video list, and write the headings line    
    csvFile = open('video_results.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["TITLE","ID","VIEWS","LIKES","DISLIKES","COMMENTS","FAVORITES"])
    
    # search for videos matching search term; write an output line for each
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
                if 'favoriteCount' not in video_results["statistics"]:
                    favoriteCount = 0
                else:
                    favoriteCount = video_results["statistics"]["favoriteCount"]
                    
            csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount])

    csvFile.close()
  
# main routine
parser = argparse.ArgumentParser(description='YouTube Search')
parser.add_argument("--search_term", default="music")
parser.add_argument("--search_max", default=30)
args = parser.parse_args()
    
youtube_search(args)


#   reading the csv file using pandas and store it in data
data=pd.read_csv('video_results.csv')

# MAX and MIN Value in the VIEWS COLUMN
Max_Views = (np.where(data["VIEWS"] == np.max(data["VIEWS"])))
print("Max Views for the video Title", data.iloc[Max_Views[0],:].TITLE)
print("Max Views for the video", data.iloc[Max_Views[0],:].VIEWS)

Min_Views = (np.where(data["VIEWS"] == np.min(data["VIEWS"])))
print("Min Views for the video Title", data.iloc[Min_Views[0],:].TITLE)
print("Min Views for the video", data.iloc[Min_Views[0],:].VIEWS)


# MAX and MIN Value in the LIKES
Max_Likes = (np.where(data["LIKES"] == np.max(data["LIKES"])))
print("Max Likes for the video Title", data.iloc[Max_Likes[0],:].TITLE)
print("Max Likes for the video", data.iloc[Max_Likes[0],:].LIKES)

Min_Likes = (np.where(data["LIKES"] == np.min(data["LIKES"])))
print("Min Likes for the video Title", data.iloc[Min_Likes[0],:].TITLE)
print("Min Likes for the video", data.iloc[Min_Likes[0],:].LIKES)


# MAX and MIN Value in the DISLIKES
Max_Dislikes = (np.where(data["DISLIKES"] == np.max(data["DISLIKES"])))
print("Max Dislikes for the video Title", data.iloc[Max_Dislikes[0],:].TITLE)
print("Max Dislikes for the video", data.iloc[Max_Dislikes[0],:].DISLIKES)

Min_Dislikes = (np.where(data["DISLIKES"] == np.min(data["DISLIKES"])))
print("Min Dislikes for the video Title", data.iloc[Min_Dislikes[0],:].TITLE)
print("Min Dislikes for the video", data.iloc[Min_Dislikes[0],:].DISLIKES)


# MAX and MIN Value in the COMMENTS
Max_Comments = (np.where(data["COMMENTS"] == np.max(data["COMMENTS"])))
print("Max Comments for the video Title", data.iloc[Max_Comments[0],:].TITLE)
print("Max Comments for the video", data.iloc[Max_Comments[0],:].COMMENTS)

Min_Comments = (np.where(data["COMMENTS"] == np.min(data["COMMENTS"])))
print("Min Comments for the video Title", data.iloc[Min_Comments[0],:].TITLE)
print("Min Comments for the video", data.iloc[Min_Comments[0],:].COMMENTS)


# SUM of values of individual column
Sum_of_Individual_Data_Columns = data.sum(axis = 0)
print(Sum_of_Individual_Data_Columns)



