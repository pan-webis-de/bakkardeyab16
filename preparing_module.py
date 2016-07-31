
import os
from sklearn import svm
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text #stopwords from sklearn
from nltk import word_tokenize
from nltk.corpus import stopwords #stopwords from nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import RegexpStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report




#----------------------------------------------------------------------
# steaming(list_documents,algorithm)
#----------------------------------------------------------------------
# input
#   list_documents - each elem of the is the data from 1 user
#   algorithm - there are meny stemming algorithm
#       0 - PorterStemmer
#       1 - LancasterStemmer
#       2 - RegexpStemmer
#       3 - SnowballStemmer (value by default
#       4 - WordNetLemmatizer
# return (the data stemmed)
#----------------------------------------------------------------------
def stemming(lines,algorithm=3):
    
    #selecting the algorithm to use
    #total 57370 in 12/11/2015
    if algorithm==0:
        #results with this algorith 56700 features
        stemmer = PorterStemmer()                           
    elif algorithm==1:
        #results with this algorith 57731 features
        stemmer = LancasterStemmer()                        
    elif algorithm==2:
        #results with this algorith 58007 features
        stemmer = RegexpStemmer('ing$|s$|e$|able$', min=4)  
    elif algorithm==3:
        #results with this algorith 56282 features (stopwords removed after stemmed)
        # 55230 if stopwords are remove first with method==2
        stemmer = SnowballStemmer("english")
    elif algorithm==4:
        #results with this algorith 56795 features
        wnl = WordNetLemmatizer()                           
    else:
        raise ValueError('Algorithm values should [0-4] ')
    
    stemmed_lines = []
    # run thru all lines
    for each_line in lines:
        a_line_stemmed = ''
        
        #tokenize each line
        tokens = each_line.split()
        
        # run thru all tokens
        for each_token in tokens:
            #do the stemming to each token and join the tokens back togther
            if algorithm==4:
                a_line_stemmed = a_line_stemmed+' '+ wnl.lemmatize(each_token)
            else:
                a_line_stemmed = a_line_stemmed+' '+ stemmer.stem(each_token)
                
        #recreate the list all over                
        stemmed_lines.append(a_line_stemmed)
    return stemmed_lines

#----------------------------------------------------------------------
# remove_stopwords(lines,method=2):
#----------------------------------------------------------------------
# input
#   lines - each elem of the is the data from 1 user
#   method - there are many stopwords list, here u can choose one method
#       0 - using nltk stopwords list
#       1 - using klearn stopwords list
#       2 - using nltk + klearn stopwords lists all toghter (default)
# return (the data with no stopwords)
#----------------------------------------------------------------------
def remove_stopwords(lines,method=2):

    if method==0:
        # using nltk stopwords
        stopwords_list = set(stopwords.words("english"))
    elif method==1:
        # using klearn stopwords
        stopwords_list = list(text.ENGLISH_STOP_WORDS)
    elif method==2:
        stopwords_list =list(set(stopwords.words("english") + list(text.ENGLISH_STOP_WORDS)))
    else:
         raise ValueError('Method value should be [0-2]')

    without_sw_lines = []
    # run thru all lines
    for each_line in lines:
        a_line_without_sw = ''
        
        #tokenize each line
        tokens = each_line.split()
        
        # run thru all tokens
        for each_token in tokens:
            if each_token not in stopwords_list:
                a_line_without_sw = a_line_without_sw+' '+each_token
                
        #recreate the list all over                
        without_sw_lines.append(a_line_without_sw)
        
    return without_sw_lines

#-------------------------------------------------------------------------------
    
def truth_file_to_dict(truth_file):
    d = {}
    d_list = []
    #open it for read
    tf = open(truth_file, 'r', encoding="utf8")

    #read the all file
    lines = tf.readlines()

    # look in to each line of the list of lines
    for each_line in lines:
        #print(each_line)
        user_info = each_line.split(':::')

        # get tokens
        userid = user_info[0]
        gender = user_info[1]
        age = user_info[2].strip()

        #print(userid)
        #print(gender)
        #print(age)

        #classification = 1000000

        if gender =='MALE':
            if age =='18-24':
                classification = 1    #male with age of 18-24 will be class=1
            if age =='25-34':
                classification = 2    #male with age of 25-34 will be class=2
            if age =='35-49':
                classification = 3    #male with age of 35-49 will be class=3
            if age =='50-64':
                classification = 4    #male with age of 50-64 will be class=4
            if age =='65-xx':
                classification = 5    #male with age of 65-xx will be class=5
        if gender=='FEMALE':
            if age =='18-24':
                classification = 6    #female with age of 18-24 will be class=6
            if age =='25-34':
                classification = 7    #female with age of 25-34 will be class=7
            if age =='35-49':
                classification = 8    #female with age of 35-49 will be class=8
            if age =='50-64':
                classification = 9    #female with age of 50-XX will be class=9
            if age =='65-xx':
                classification = 10   #female with age of 65-xx will be class=10
                print(classification)

        # print(classification)
        # create an empty dictionary
        d[userid] = {'gender':user_info[1],'age':user_info[2],'class': classification}

        d_list.append(d[userid])
    #close the file
    tf.close()
    
    return (d)

#----------------------------------------------------------------------
# bag_of_words_test(list_documents,max_features)
#----------------------------------------------------------------------
# input
#   list_documents - each elem of the is the data from 1 user
#   max_features - force the bag of words to have a max of features
# return a list with all words from the bag
#----------------------------------------------------------------------
def bag_of_words_to_list(lines,max_features):
    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool
    # removing stopwords
    vectorizer = CountVectorizer(
        stop_words = 'english'
        ,max_features = max_features
        )
    
    #TfidfVectorizer i need to check this

    print('>> Removing stopwords...')
    # lets remove stopwords
    lines = remove_stopwords(lines,2)

    print('>> Stemming...')
    # lets stem it
    lines =stemming(lines,3)

    print('>> Doing bag of words...')
    #lets do the bag of words
    bag_of_words = vectorizer.fit_transform(lines)



    #uncomment to visualize the words and how many times are used
    #printing_bow(bag_of_words,vectorizer)

    return(vectorizer.get_feature_names(),bag_of_words.toarray())



#----------------------------------------------------------------------
# read_all_files()
#----------------------------------------------------------------------
# input
#       nothing, but uses destiny folder
# return (the data form all users with §i and §f stripped out)
#----------------------------------------------------------------------
def read_all_files(destiny_folder):
    # get the list of files of the source_folder
    files = os.listdir(destiny_folder)

    print('>> Reading data files...')
    all_data = []
    userid_list = []
    # get a file at a time from the list
    for each_file in files:

        #print(each_file)
        
        #open it for read
        fs = open(destiny_folder+each_file, 'r',encoding="utf8")

        #read the all file
        all_text = fs.read()

        #parse the file spliting for the §i and §f tokens
        all_text = all_text.replace('§f\nÂ§i','')
        all_text = all_text.replace('§i','')
        all_text = all_text.replace('§f','')

        
        #-----------------------------------------------------------------------
        #just a comparison it should be commented
        #comparing_bow_with_without_stopwords(lines)

        all_data.append(all_text)

        #extract user ID from the file name
        userid = each_file[:-4]
        userid_list.append(userid)
        
        #close the source file
        fs.close()
    return (userid_list,all_data)

#-------------------------------------------------------------------------------

import math
def read_bag_of_words(size, destiny_folder, truth_file):

    userids_list,data = read_all_files(destiny_folder)

    #create a bag of words and return the list of words
    words_list,data=bag_of_words_to_list(data,size)

    # getting the data from the turth file
    truth_dict = truth_file_to_dict(truth_file)

    features = []
    for ui in range(len(userids_list)):
        userid = userids_list[ui]
        
        dictionary = dict.fromkeys(words_list, 0)
        dictionary[' userid'] = userid

        dictionary[' _class'] = truth_dict[userid]['class']
        dictionary[' age'] = truth_dict[userid]['age']
        dictionary[' gender'] = truth_dict[userid]['gender']

        for wi in range(len(words_list)):
            dictionary[words_list[wi]] = math.log(data[ui][wi]+1)
        features.append(dictionary)
       
    return(features)
    #return (used_words_list)

