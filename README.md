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

![alt text](https://github.com/crenshawj/rt-movie-project/blob/main/images/rtCritic%20-%20rtAudience%20top%2030.PNG)  

As you can see, this is not exactly Best Picture material.  Most movies are pretty familiar including Transformers, Pirates of the Caribbean, and Twilight.  One which I haven’t heard of is “The Golden Child” starring Eddie Murphy.  It’s about a private detective who is trying to find a missing child that has supernatural powers.  This one sounds pretty good.  I’m going to put it on my watch list.   

*Finding a link between Critic/Audience Review Scores and Box Office Receipts*  

In order to see if there is a relationship between review scores and Gross Box Office amounts, I calculated correlations between Adjusted Box Office Totals and several variables.    
(Correlations w/ adjusted Gross and different measures of critic/audience scores)  
![alt text](https://github.com/crenshawj/rt-movie-project/blob/main/images/correlations.PNG)  

Here we can see that “rt_audience_score” (average audience review score) had the highest correlation with Adjusted Box Office amounts at .3933.  This means that 39.33% of the variation in Adjusted Box Office Totals can be explained by audience review scores.  IMDB rating had the 2nd highest at .2677, and “rt_score” (average critic score) had the 3rd highest.  
It’s interesting that audience scores seem to have a bigger impact than critic scores on a movie’s Box Office amount.    

Another way to visualize the relationship between average audience review scores and box office receipts is by using a scatter plot.

Here is a scatter plot showing the relationship between rt_audience_score (average user review) and Adjusted Box Office totals:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```matplotlib.pyplot.scatter(scoreList,adjustedList)```  
![alt text](https://github.com/crenshawj/rt-movie-project/blob/main/images/scatter%20plot.PNG)  

The red line represents a line of best fit, which is a line that minimizes the squared vertical distances betweeen the observed y's (observed box office amounts) and the predicted y's (The predicted y values are all the points on the line).  

Based on the scatter plot and the line of best fit, it appears there is a moderate positive correlation between average audience ratings and box office receipts.   By taking the slope of the best fit line, we can quantify this relationship.  The equation for the line is y = 354.36x + -687.46.  This means that for every 1 point increase in audience rating, there is an observed $354 million increase in box office receipts. 

Upon examining the data further, I noticed that the box office amounts were heavily skewed. 
You can see this clearly in the histogram below.  
Using  
&nbsp;&nbsp;&nbsp;```dataframe['adjusted'].plot(kind='hist') and matplotlib.pyplot.show()```  
we can get a histogram of the Adjusted Box Office column:  
![alt text](https://github.com/crenshawj/rt-movie-project/blob/main/images/histogram%20box%20office.PNG)  







