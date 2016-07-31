
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
import preparing_module


def test_params(target,data):
    import warnings
    warnings.filterwarnings("ignore")
    X = data
    y = target


    # Split the dataset in two equal parts
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=0)
    
    # Set the parameters by cross-validation
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [0.0001, 0.001, 0.01,0.1,1,10,100,1000,10000],
                     'C': [0.0001,0.001,0.01,0.1,1, 10, 100, 1000,10000]},
                    {'kernel': ['linear'], 'C': [1,10]}]

    #scores = ['precision', 'recall']
    scores = ['precision']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        
        clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=3,
                           scoring='%s' % score)
     
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()

        train_with_best_params(clf.best_params_, target, data)


#///////////////////////////////////////////////////////////////////////////////
def train_with_best_params(bp, target, data):
    k = bp['kernel']
    if(k=='linear'):
        c = bp['C']
        clf = svm.SVC(C=c,kernel=k)
        clf.fit(data, target)
        with open('model.pkl', 'wb') as fid:
            pickle.dump(clf, fid)
    else:
        c = bp['C']
        g = bp['gamma']
        clf = svm.SVC(C=c,kernel=k,gamma=g)
        clf.fit(data, target)
        with open('model.pkl', 'wb') as fid:
            pickle.dump(clf, fid)        



def main(argv):

    destiny_folder = argv[0]
    truth_file = argv[1]

    number_of_features = 100

    # create the bag of words if needed

    features_list = preparing_module.read_bag_of_words(number_of_features, destiny_folder, truth_file)


    #print(features_list)


    df = pd.DataFrame(features_list)


    target = df.values[:,0].tolist()
    data = df.values[:,4:].tolist()

    test_params(target,data)



if __name__ == "__main__":
    main(sys.argv[1:])




# python3 training.py /home/rodwan/Desktop/doctorate/ML/TIRA/codes/tagged_dataset/ /home/rodwan/Desktop/doctorate/ML/TIRA/codes/PAN161/truth.txt
