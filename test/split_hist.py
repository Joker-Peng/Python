import pandas as pd
from dython.data_utils import split_hist
from sklearn.linear_model import LogisticRegression
from dython.model_utils import ks_abc
import numpy as np
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from dython.model_utils import metric_graph

def zhu():
    # Load data and convert to DataFrame
    data = datasets.load_breast_cancer()
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    df['malignant'] = [not bool(x) for x in data.target]

    # Plot histogram
    split_hist(df, 'mean radius', split_by='malignant', bins=20, figsize=(15, 7))

def mu():
    # Load and split data
    data = datasets.load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=.5, random_state=0)

    # Train model and predict
    model = LogisticRegression(solver='liblinear')
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)

    # Perform KS test and compute area between curves
    ks_abc(y_test, y_pred[:, 1])

def mg():
    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = label_binarize(iris.target, classes=[0, 1, 2])

    # Add noisy features
    random_state = np.random.RandomState(4)
    n_samples, n_features = X.shape
    X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

    # Train a model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)
    classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True, random_state=0))

    # Predict
    y_score = classifier.fit(X_train, y_train).predict_proba(X_test)

    # Plot ROC graphs
    metric_graph(y_test, y_score, 'pr', class_names=iris.target_names)

def mg2():
    # Load data
    iris = datasets.load_iris()
    X = iris.data
    y = label_binarize(iris.target, classes=[0, 1, 2])

    # Add noisy features
    random_state = np.random.RandomState(4)
    n_samples, n_features = X.shape
    X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]

    # Train a model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)
    classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True, random_state=0))

    # Predict
    y_score = classifier.fit(X_train, y_train).predict_proba(X_test)

    # Plot ROC graphs
    metric_graph(y_test, y_score, 'roc', class_names=iris.target_names)

if __name__ == '__main__':
    # zhu()
    # mu()
    # mg()
    mg2()