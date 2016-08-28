
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
import pickle
import sys
import preparing_module_testing as pmt
import warnings



def testing(target, data, model_path, output_path):

    ag = ['18-24', '25-34', '35-49', '50-64', '65-xx', '18-24', '25-34', '35-49', '50-64', '65-xx']
    g = ['male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male', 'male']

    with open(model_path, 'rb') as fid:
        gnb_loaded = pickle.load(fid)

    #target1 = []

    
    frrr = open("output.txt", 'w',encoding="utf8")
    t = 0
    for d in data:        
        p = gnb_loaded.predict(d)
        print(p)
        fr = open(output_path+target[t]+".xml", 'w',encoding="utf8")        
        fr.write(' <author id="{'+target[t]+
            '}"\n         type="twitter" \n         lang="en" \n         age_group="'+ag[p-1]+'"\n         gender="'
            +g[p-1]+'"\n />\n')                
        frrr.write(target[t] + "    "+ ag[p-1] +"   " +g[p-1]+"\n")
        t = t + 1



def main(argv):

    warnings.filterwarnings('ignore')

    source_folder = argv[0]
    model_path = argv[1]
    output_path = argv[2]
    #truth_file = argv[1]

    number_of_features = 10000

    # create the bag of words if needed

    features_list = pmt.read_bag_of_words(number_of_features, source_folder)


    #print(features_list)

    df = pd.DataFrame(features_list)




    target = df.values[:,0].tolist()
    data = df.values[:,1:].tolist()



    testing(target, data, model_path, output_path)




if __name__ == "__main__":
    main(sys.argv[1:])


# python3 testing.py ./tagged_dataset/ ./model.pkl ./output/
