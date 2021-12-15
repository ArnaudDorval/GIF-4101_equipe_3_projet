from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def decision_random_tree_models(data, list):
    X, y = data()
    max_it = range(1, 100)
    max_depth = range(1, 20)
    max_ft = range(1, 2)
    tmp_score = 0

    best_max_iter = 0
    best_estimator = 0
    best_max_ft = 0
    best_clf = DecisionTreeClassifier()

    X_train, X_test, y_train, y_test = train_test_split(X[list], y, test_size=0.25)
    #print("")


    for j in max_it:
        for k in max_depth:
            clf = RandomForestClassifier(max_depth=k, n_estimators=j, max_features=1)
            clf.fit(X_train, y_train)
            #clf.predict(X_test)
            new_score = clf.score(X_test, y_test)
            if new_score > tmp_score:
                tmp_score = new_score
                best_clf = clf
                best_max_iter = k
                best_estimator = j



    print("random tree classifier :,Score = {0}, max_depth = {1},"
          "max_estimator = {2}, Comment = {3}"
        .format(best_clf.score(X_test, y_test), best_max_iter, best_estimator,  ""))