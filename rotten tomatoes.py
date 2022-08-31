#consider making average score:
#audience = .5*(audience_freshness+rt_audience)
#rotten = .5*(rt_freshness+rt_score)

import pandas,os,re,math,matplotlib.pyplot

#set cwd to where csv file is located
os.chdir(r'C:\Users\Admin\Desktop\ATBS Python\ATBS programs\programs 9-30-21\ch11 files (Web Scraping)\Ch11 BeautifulSoup\rotten tomato movie project')

dataframe = pandas.read_csv('blockbuster-top_ten_movies_per_year_DFE.csv')

#print(dataframe,end='\n') #print first 5 rows and last 5 rows
#print(dataframe.head(10)) #print first 10 rows
#print(dataframe.tail(10)) #print last 10 rows

print(dataframe.info());print()
#pandas.options.display.max_columns=20

#cleaning the data
print('Null row(2nd to last row): ')
print(dataframe.loc[397]);print()

#remove 2nd to last row (#397) b/c the whole row is null
dataframe.drop(397,inplace=True)

#rename row 398 to row 397 b/c we dropped row 397
dataframe.rename(index={398:397},inplace=True)

print('After dropping null row: ')
print(dataframe.info());print()

#drop columns you don't need
genres=['genres','Genre_2','Genre_3','studio']
dataframe.drop(genres,axis=1,inplace=True)

print('After dropping unnecessary columns: ')
print(dataframe.info());print()

#determine duplicates using posterURL+title b/c
#King King(1970) and King King(2005) are 2 different movies
#also there were two movies w/ different titles
#but had the same poster URL
#(posterURL+title acts as like a unique ID for each row)

#print rows with duplicate movie titles
print('\nRows with Duplicate titles: ')
for title in dataframe['title']:
    #df is a new dataframe consisting of just rows w/ duplicate titles
    df=dataframe[dataframe['title']==title]
    if len(df)>1: print(df[['title','year']])

#print rows with duplicate poster URL
print('Movie titles with duplicate Poster URLs: ')
for posterURL in dataframe['poster_url']:
    df=dataframe[dataframe['poster_url']==posterURL]
    if len(df)>1: print(df[['title','year']])

#add column combining posterURL and Movie title to df
dataframe['posterURL_title']=dataframe.poster_url+dataframe.title

#print rows with duplicate posterURL+title
print('\nRows with duplicate URL+title: ')
for urlTitle in dataframe['posterURL_title']:
    df=dataframe[dataframe['posterURL_title']==urlTitle]
    if len(df)>1: print(df[['title','year']])

print('\nNumber of url+title in dataframe: '+str(len(dataframe['posterURL_title'])))
posterURL_set = set(dataframe.posterURL_title)
print('Number of unique url+title: '+str(len(posterURL_set)))

#keep first entry that's a duplicate
dataframe.drop_duplicates(subset=['poster_url','title'],inplace=True,keep='first')
print('\nAfter dropping duplicate rows based on posterURL+title: ')
print(dataframe.info())

#rename indexes after dropping duplicates
#dataframe.reset_index(drop=True,inplace=True)
#list(range(10)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
dataframe.index = range(len(dataframe.index)) #len(dataframe) == len(dataframe.index)

#double check for duplicates
urlTitleList=[] #list of poster URL + title
for index in dataframe.index: #for i in range(len(dataframe))
    #the reason to use index instead of for i in range(len(dataframe))
    #is in case u forget to rename the indexes after dropping rows
    posterURL = dataframe.loc[index]['poster_url']
    title = dataframe.loc[index]['title']
    urlTitleList.append(posterURL+title)

print('\nNumber of url+title in dataframe: '+str(len(dataframe['posterURL_title'])))
urlSet = set(urlTitleList)
print('Number of unique url+title: '+str(len(urlSet)),end='\n')

#delete rows where rt_score==0
#dataframe.rt_score==0 returns a list of bool values for every row (True if rt==0)
#dataframe[dataframe.rt_score==0] returns just rows where rt_score==0
#dataframe[dataframe.rt_score==0].index is just the index values where rt_score==0
#drop rows where rt_score==0:
dataframe.drop(dataframe[dataframe.rt_score==0].index,inplace=True)

#reset indexes after filtering out RT score of 0
dataframe.index = range(len(dataframe.index))

print('\nAfter deleting rows w/ rt_score == 0.\n')
print(dataframe.info(),end='\n\n')

#create avg audience and rt scores as new columns
dataframe['avg_audience']=10*dataframe.rt_audience_score+.5*dataframe.audience_freshness
dataframe['avg_rt']=.5*(dataframe.rt_freshness+10*dataframe.rt_score)
print('Added avg audience and avg rt columns.')
print(dataframe.info(),end='\n\n')

def sortTable(column1,column2,displayP,sortP):
    #use if you want to sort based on existing columns
    #displayP = number to display
    #sortP: 'Bottom' == asc, default is Desc
    columnDict = {'imdb_rating':'IMDB','avg_audience':'Avg Audience','avg_rt':'Avg RT',
                  'rt_audience_score':'RT Audience Score','audience_freshness':'Audience Freshness'}
    txt1=columnDict[column1]; txt2=columnDict[column2]
    if sortP == 'Desc':
        dataframe.sort_values([column1,column2],ascending=False,inplace=True)
    else:
        dataframe.sort_values([column1,column2],ascending=True,inplace=True)
    print('Top '+str(displayP)+' results '+txt1+' '+sortP+', '+txt2+'(tie-breaker):')
    i = 0; print('       Title            '+'  '+txt1+'  '+txt2)
    for index in dataframe.index:
        if i > displayP: break
        var1 = dataframe.loc[index][column1]
        var2 = dataframe.loc[index][column2]
        title = dataframe.loc[index]['title']; space = ' '*(33-len(title))
##        print('Title: '+title+space+txt1+': '+str(var1),end=' ')
##        print(txt2+': '+str(var2)); i+=1
        print(title[:33]+space+' '+str(var1)+' '*15+str(var2));i+=1
    #reset indexes?
    #dataframe.index = range(len(dataframe.index))

def addColumn(colNameP,column1,column2,symbolP):
    #column1 and column2 are 2 columns you want to avg
    #if symbol == '+', avg columns, if '-', subtract columns
    multDict = {'imdb_rating':10,'rt_audience_score':2} #get factor to multiply column
    mult1 = multDict.get(column1,1)
    mult2 = multDict.get(column2,1)
    column1 = mult1*dataframe[column1]
    column2 = mult2*dataframe[column2]
    if symbolP=='+': dataframe[colNameP]=.5*(column1+column2) #avg
    if symbolP=='-': dataframe[colNameP]=column1-column2 #subtract
    return mult1    

def sortTableAvg(column1,column2,displayP,symbol,sortP,tieP):
    #Use if you want to add new column to table and sort based on that
    #displayP = number to display; symbol="+"or'-' for addColumn function
    #tieP = whether u want 1st or 2nd column to be tiebreaker
    columnDict = {'imdb_rating':'IMDB','avg_audience':'Avg Audience','avg_rt':'Avg RT',
                  'rt_audience_score':'rtAudience','rt_score':'rtCritic','rt_freshness':'RT Freshness'}
    txt1=columnDict[column1]; txt2=columnDict[column2]
    colName = (txt1+symbol+txt2).strip()
    mult = addColumn(colName,column1,column2,symbol)
    print('Top '+str(displayP)+' movies '+sortP+' '+colName+', ',end='')
    if tieP == 1:
        print(column1+'(tie-breaker):')
        if sortP == 'Desc':
            dataframe.sort_values([colName,column1],ascending=False,inplace=True)      
        else:
            dataframe.sort_values([colName,column1],ascending=True,inplace=True)
    if tieP == 2:
        print(column2+'(tie-breaker):')
        if sortP == 'Desc':
            dataframe.sort_values([colName,column2],ascending=False,inplace=True)      
        else:
            dataframe.sort_values([colName,column2],ascending=True,inplace=True)
    #if ('+' or '-') in critDict[column1] == True:
        #txt1 = re.split('\+|-',critDict[column1])[0]
    print('       Title            '+colName+' '+column1+' '+column2)
    i = 0 
    for index in dataframe.index:
        if i > displayP: break
        var1 = dataframe.loc[index][colName]
        var2 = dataframe.loc[index][column1]
        if column1 in ['imdb_rating','rt_audience_score']: var2=mult*var2
        var3 = dataframe.loc[index][column2]
        if column2 in ['imdb_rating','rt_audience_score']: var3=mult*var3
        title = dataframe.loc[index]['title'][:33]; space = ' '*(33-len(title))
##        print('Title: '+title+space+colName+': '+str(var1),end=' ')
##        print(txt1+': '+str(var2)+' '+txt2+': '+str(var3)); i+=1
        print(title+space+' '+'%.1f'%var1+'             '+str(var2)+'          '+str(var3))
        i+=1
    #reset indexes?
    #dataframe.index = range(len(dataframe.index))
        
#sortTable('rt_audience_score','audience_freshness',30,'Desc')
sortTableAvg('rt_audience_score','rt_freshness',30,'-','Desc',1)
#sortTableAvg('avg_audience','avg_rt',30,'-','Desc',1)

#Convert adjusted gross from str to float
#Have to remove whitespace, commas, and $ first
#remove whitespace from adjusted gross column
dataframe['adjusted'] = dataframe['adjusted'].str.strip()

#remove dollar sign, commas
for index in dataframe.index:
    #remove dollar sign
    dataframe.loc[index,'adjusted'] = dataframe.loc[index,'adjusted'][1:]
    #remove commas
    dataframe.loc[index,'adjusted'] = dataframe.loc[index,'adjusted'].replace(',','')
##    #convert to float
##    dataframe.loc[index,'adjusted'] = float(dataframe.loc[index,'adjusted'])

#Convert adjusted gross from str to float
dataframe['adjusted'] = dataframe['adjusted'].astype(float)

#rt_audience_score == avg audience review score
print('\nCorrelation between adjusted Gross and Avg Audience Review Score:') 
print('%0.4f'%dataframe['adjusted'].corr(dataframe['rt_audience_score']))

##graph = dataframe.plot(kind='scatter',x='rt_audience_score',y='adjusted')
##graph.set_ylabel('Adjusted Gross in Billions USD')
##matplotlib.pyplot.show()

#dataframe['adjusted'][:10] #display first 10 entries in adjusted column

#get list of X(scores) and Y(box office) 
scoreList = []; adjustedList = []
for item in dataframe['rt_audience_score']: scoreList.append(item) #X
for item in dataframe['adjusted']: adjustedList.append(item) #Y

#y = m*x + b; solve for m and b
def best_fit(X, Y, adjustP):
    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    denom = sum([xi**2 for xi in X]) - n * xbar**2
    numer = float(numer); denom = float(denom)

    m = numer / denom; mFormat=m/(10**6) #slope in millions($)
    b = ybar - m * xbar; bFormat=b/(10**6)

    if adjustP in ['Y','Yes']: print('best fit line:\ny = {:.2f}x + {:.2f}'.format(mFormat,bFormat))
    else: print('best fit line:\ny = {:.4f}x + {:.2f}'.format(m,b))
    return m, b

#scatter plot w/ line of best fit (Adj. Gross vs RT Audience Score)
m,b = best_fit(scoreList,adjustedList,'Y') #get slope and intercept

#get standard error to determine t stat of slope of best fit line
def getSE(X,Y,yHatsP): #yHats = predicted y values from best fit line
    xbar = sum(X)/len(X)
    n = len(X) # or len(Y)

    numer = sum([(yi-yHat)**2 for yi,yHat in zip(Y,yHatsP)])
    numer = (numer / (n-2))**.5 #392 is size of sample (# of movies in dataframe)
    denom = sum([(xi-xbar)**2 for xi in X])
    denom = denom**.5 #square root
    stdError = numer / denom
    return stdError
yHats_bo = [] #hold list of predicted y(box office) values based on best fit line
for score in scoreList: #loop thru x values (scores) to find predicted y vals(box office)
    yHat_bo = m*score+b #predicted box office value
    yHats_bo.append(yHat_bo)
se = getSE(scoreList,adjustedList,yHats_bo) #t stat for slope = slope/std error
#print('Std Error of slope is %.2f'%(se/10**6))

matplotlib.pyplot.scatter(scoreList,adjustedList)
yfit = [m*xi+b for xi in scoreList]
matplotlib.pyplot.plot(scoreList,yfit,color="red") #plot line
matplotlib.pyplot.xlabel('RT Audience Score') 
matplotlib.pyplot.ylabel('Adjusted Gross in Billions USD')
matplotlib.pyplot.show()

#plot histogram of adjusted box office totals
hist = dataframe['adjusted'].plot(kind='hist')
hist.set_xlabel('Adjusted Box Office (Billions $USD)')
matplotlib.pyplot.show()

#histogram of box office amounts shows that the distribution is extremely skewed
#transform box office amounts into logs before finding correlation and best fit line?

#create new column of natural log of adjusted box office values
##lnAdj=[]
##for index in dataframe.index:
##    boVal = dataframe.loc[index]['adjusted']
##    lnAdj.append(math.log(boVal))
lnAdj = [] #hold list of natural log values
for boVal in dataframe['adjusted']: lnAdj.append(math.log(boVal)) #add ln(boxOffice) to list
dataframe['ln_adjusted'] = lnAdj #create new column to hold natural log values

hist = dataframe['ln_adjusted'].plot(kind='hist') #plot histogram of transformed box office amounts
hist.set_xlabel('Natural Log of Box Office')
matplotlib.pyplot.show()

#get new best fit line
m,b = best_fit(scoreList,lnAdj,'N') #get slope and intercept
#plot scatter plot using transformed y values
matplotlib.pyplot.scatter(scoreList,lnAdj)
yfit = [m*xi+b for xi in scoreList]
matplotlib.pyplot.plot(scoreList,yfit,color="red") #plot line
matplotlib.pyplot.xlabel('RT Audience Score') 
matplotlib.pyplot.ylabel('Natural Log of Box Office')
matplotlib.pyplot.show()
