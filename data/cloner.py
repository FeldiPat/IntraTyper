import os

import git

data = 'repo-SHAs.txt'
with open(data) as fp:
    line = fp.readline()
    while line:
        name = line.split(' ')
        head = name[0].split('/')[0]
        sha = str(name[1])
        repoName = 'Repos/' + name[0]
        if not os.path.isdir(repoName):
            os.makedirs(repoName)
            print("cloning " + name[0])
            try:
                repo = git.Repo.clone_from('https://github.com/' + name[0], repoName)
            except:
                print(name[0] + " not found.")
                pass
        line = fp.readline()
