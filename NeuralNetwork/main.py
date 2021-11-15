from data import Data
from non_parametric import non_parametric_models
from linear import linear_models
from SVM import svm

def main():
    data = Data()

    non_parametric_models(data)
    linear_models(data)
    svm(data)


if __name__ == "__main__":
    main()
