import datetime

import git
from git import *
from datetime import date
import os
import logging

# PATH_OF_GIT_REPO = r'C:/Users/arnau/OneDrive/Documents/Universite/Automne 2021/AI/projet/GIF-4101_equipe_3_projet.git'  # make sure .git folder is properly configured
PATH_OF_GIT_REPO = r'C:\Users\arnau\OneDrive\Documents\Universite\Automne 2021\AI\projet\GIF-4101_equipe_3_projet\.git'
HTTPS_REPO = 'https://github.com/ArnaudDorval/GIF-4101_equipe_3_projet.git'
COMMIT_MESSAGE = 'test python push'
logging.basicConfig(filename='test.log', level=logging.DEBUG)


def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    t = git.Repo(PATH_OF_GIT_REPO)
    o = repo.remotes.origin
    o.pull()
    repo.git.add(all=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()


file_name = 'data/' + str(date.today()) + "-test.txt"

try:
    f = open("test_txt.txt", 'w')
    f.write("Allo ce ceci est un test")
    f.close()

    git_push()

except:
    logging.info(str(datetime.datetime.now()))
    logging.exception('')
