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

# Database Setup

1. migrations 폴더에 있는 __init__.py 제외 모든 파일 삭제
2. db.sqlite3 삭제
-> 데이터베이스가 기존것과 중복으로 오류가 날 수 있기 때문에 삭제 후 사용하시는 것을 추천드립니다!
`$ python manage.py makemigrations`
`$ python manage.py migrate`
`$ python dbconn.py`

## 데이터베이스 확인하기

`$ python manage.py dbshell`
`>>> .table`
sql 사용하여 각 테이블에 들어있는 값 확인하기


## crontab 사용법

requirements.txt 실행

작업 등록
`$ python manage.py crontab add`

작업 등록 확인
`$ python manage.py crontab show`

작업 삭제
`$ python3 manage.py crontab remove`

등록한 작업 id값으로 그냥 실행 (id 값은 show했을때 나오는 id값)
`$ python3 manage.py crontab run <hash_id>`
