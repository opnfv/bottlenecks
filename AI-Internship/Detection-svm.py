import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
from sklearn.model_selection import train_test_split
get_ipython().magic('matplotlib inline')

data = pd.read_csv("posca_factor_ping-final.csv",usecols=[2,3,4,5,6],engine='python')  

x = data.drop('result', axis=1)  
y = data['result']  
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.35)  
svclassifier = SVC(kernel='linear')  
svclassifier.fit(X_train, y_train)  

y_pred = svclassifier.predict(X_test)  

from sklearn.metrics import classification_report, confusion_matrix  
print(confusion_matrix(y_test,y_pred))  
print(classification_report(y_test,y_pred))  
print(accuracy_score(y_test, y_pred)) 

from sklearn.svm import SVC  
svclassifier = SVC(kernel='poly', degree=8)  
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)  

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score 
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred))  
print(accuracy_score(y_test, y_pred)) 

#Gaussian Kernel
from sklearn.svm import SVC  
svclassifier = SVC(kernel='rbf')  
svclassifier.fit(X_train, y_train)  

y_pred = svclassifier.predict(X_test)  

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score 
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred))  
print(accuracy_score(y_test, y_pred)) 

