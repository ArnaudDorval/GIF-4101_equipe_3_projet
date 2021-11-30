from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def decision_tree_models(data):
    X, y = data()
    max_it = range(1, 20)
    tmp_score = 0

    best_max_iter = 0
    best_clf = DecisionTreeClassifier()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    print("")
    for k in max_it:
        clf = DecisionTreeClassifier(random_state=0, max_depth=k)
        clf.fit(X_train, y_train)
        new_score = clf.score(X_test, y_test)
        if new_score > tmp_score:
            tmp_score = new_score
            best_clf = clf
            best_max_iter = k


    print("decision tree :,Score = {0}, max_iter = {1}, Comment = {2}"
        .format(best_clf.score(X_test, y_test), best_max_iter, ""))
