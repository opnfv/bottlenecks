import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
data = pd.read_csv("posca_factor_ping-final.csv", usecols=[2, 3, 4, 5, 6], engine='python')
x = data.drop('result', axis=1)
y = data['result']
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.35, random_state=0)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
rrf_model = RandomForestClassifier(max_depth=10, n_estimators=10)
rrf_model.fit(X_train, y_train)
y_pred = rrf_model.predict(X_test)
result = confusion_matrix(y_test, y_pred)
print(result)
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))
sns.heatmap(
    result, annot=True, fmt='.2f', xticklabels=["FAIL", "PASS"], yticklabels=["FAIL", "PASS"])
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.title('Random Forest')
plt.savefig('random_forest')
