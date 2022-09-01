# rt-movie-project
Using python and pandas to analyze a rotten tomato dataset

Objectives:  
1)Obtain a list of movies sorted by their critic score - audience score  
2)To see if there is a link or relationship between critic/audience reviews and box office amounts

Column Definitions:  
<b>rt_audience_score</b> - average rating of audience reviews.  From 0 to 5 stars.   
Min found in data: 2.5 ,Max found in data:4.4
audience_freshness - % of audience reviews that are positive(favorable).  
<b>rt_freshness</b> - % of critic reviews that are positive(favorable).  
<b>rt_score</b> - average rating of critic reviews.  From 0 to 10.   
Min found in data: 2.7  ,Max found in data: 9.1    
<b>adjusted</b> -  worldwide box office totals adjusted for inflation  
Minimum val: $110,047,509.57 Max value: $3,025,614,789.35   
<b>imdb_rating</b> - movie rating on IMDB from 0 to 10  

Process:  
1)Get Data -> 2)Clean Data -> 3)Analyze Data -> 4)Draw Conclusions  

Step 1): Getting the Data
The data set was obtained from https://data.world/datasets/open-data
This is what the data set looks like:  
![alt text](https://github.com/crenshawj/rt-movie-project/blob/main/images/rotten%20tomato%20dataset.PNG)  

Step 2:) Cleaning the Data  
There were several issues with the dataset that I had to deal with before I could begin analyzing the data:  
1)**Getting rid of redundant columns**  
There were a few columns that had missing data or I simply didn’t need:  
These columns included Genre 2, Genre 3, and Studio (Warner,Paramount,Universal etc.) and several others.   
2)**Getting Rid of Empty Rows**  
The data set contains 399 rows not counting the header row  
Row 398 was completely blank for some reason so I removed this line using the Pandas drop() function:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```dataframe.drop(397,inplace=True)  #397 b/c the 1st row is 0, 2nd row is 1 etc.```    
3)**Getting Rid of Duplicate Rows**  
Finding duplicate rows was a little tricky.  You can’t just go off the movie title alone b/c there are some movies that have the same title.  For example rows 96 and 385 were both titled ‘King Kong’ because there was the original released in 1976 and then a reboot released in 2005.    
Therefore I used a combination of the movie poster URL + movie title to determine which rows were duplicates.    
Rows 126 and 397 were duplicates therefore I kept the first occurence (row 126) and dropped row 397:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```dataframe.drop_duplicates(subset=['poster_url','title'],inplace=True,keep='first')```  
4)**Remove rows where RT Score == 0.**  
There are 2 different measures of critic score in the dataset:    
   1)**RT Freshness**, this is the one most people are familiar with.  It’s a percentage from 0 to 100 that measures the % of critic reviews that are favorable.    
   2)**RT Score:** This is the average critic review score.  It goes from 0 to 10.   When looking at the data, I found that any movie with an RT Score of 0 (average critic review score), simply had no critic reviews.  Therefore I decided to filter out any movies w/ an RT score equal to 0.      
There were 4 rows that had an RT Score of 0 (no critic reviews).   
  
After making all these changes to the dataset I was left with 17 columns and 392 rows.  Now I could finally begin analyzing the data.    

Step 3) **Analyzing the Data**  

*Getting top 30 movies by their Audience - Critic Score*

One of my goals in doing this project was getting a list of movies that were well received by audiences but reviewed poorly by critics.  I’ve found that movies that had high critic ratings more often than not dealt with heavy emotional themes and/or were trying to push a certain political agenda.  My reasoning for sorting movies by their Audience - Critic score is to find movies that are entertaining without being too heavy in subject matter.  Since there are two measures of critic sentiment and two measures of audience sentiment I created two new columns: avg_rt and avg_audience.  Avg_rt averages the rt_freshness (% of reviews that are positive) with rt_score (avg critic review score).  Avg_audience is an average of the rt_audience_freshness column (% of user reviews that are favorable) and the rt_audience_score column (average user review score).  Then I wrote a function that uses these two new columns to sort the dataframe by the difference of Avg_audience - Avg_rt.  
Here are the results:  

