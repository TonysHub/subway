# Setting up Python version to 3.10.0

Check if you have pyenv installed
```
$ pyenv --version
```


## Setup
#### Getting pyenv

**Skip this step if you already have pyenv**

```
$ update brew
$ brew install pyenv
$ open ~/.zshrc
```

Add the following lines to ~/.zshrc or ~/.zprofile for zsh.
For bash, add to ~/.bash_profile or ~/.profile

```
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```
#### Clone project
Move to your project DIR
```
$ git clone https://github.com/TonysHub/subway.git
```



#### Install Python version


At your home DIR,
```
$ pyenv install 3.10.0
```
Open project DIR
```
$ pyenv shell 3.10.0

# check python version at this point
$ python3 --version
>>> Python 3.10.0
```

#### Setup venv
At your project DIR (~/subway)
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

Now our setup is good to go :)

# Project Git Convention
## What to do before you start coding
Open your local directory
```
$ git pull
```
if there's a conflict, try
```
$ git stash
$ git pull
$ git stash pop
```
if there's still a conflict, try
```
$ git reset --hard
$ git pull
```
Check which branch you are on
```
$ git branch
```
If you are not on the branch you want to be on, try
```
$ git checkout <branch_name>
```
If you want to create a new branch, try
```
$ git checkout -b <branch_name>
```

## What to do after you finish coding
Check which files you have changed
```
$ git status
```
Add the files you want to commit
```
$ git add <file_name>
```
Commit the files
```
$ git commit -m "<commit_message>"
```
Push the files to your branch
```
$ git push origin <branch_name>
```
If you want to merge your branch to the main branch, go to github and create a pull request :)

## Branch naming convention
Branch name should be in lower case and separated by underscore. Your initials at the beginning, and select from [feature, bugfix, refactor, etc] for the middle part. The last part should be the feature name.

Ex. 
```
git branch -b lds_feature_datascrapping
```

## Commit message convention
commit_message should be concise and imply what you have done. If you are fixing a bug, start with "fix: ", if you are adding a feature, start with "add: ", etc.

Ex.
```
git commit -m "fix: fix bug in datascrapping"
```


