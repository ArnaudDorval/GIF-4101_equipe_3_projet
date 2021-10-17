from git import Repo
from datetime import date
import os
import logging

#PATH_OF_GIT_REPO = r'C:/Users/arnau/OneDrive/Documents/Universite/Automne 2021/AI/projet/GIF-4101_equipe_3_projet.git'  # make sure .git folder is properly configured
PATH_OF_GIT_REPO = r'C:\Users\arnau\OneDrive\Documents\Universite\Automne 2021\AI\projet\GIF-4101_equipe_3_projet\.git'
COMMIT_MESSAGE = 'test python push'


def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()
    #        print('Some error occured while pushing the code')


file_name = 'data/' + str(date.today()) + "-test.txt"

f = open("test_txt.txt", 'w')
f.write("Allo ce ceci est un test")
f.close()

git_push()
