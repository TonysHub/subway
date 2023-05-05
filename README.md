# serializer feed in process
1. 데이터 베이스 초기화하기
- migrations 폴더 내 ```__init__.py``` 제외하고 모두 제거
- ```db.splite3``` 제거
- ```pyhton manage.py makemigrations```
- ```python manage.py migrate```
- ```python daily_process.py```

수정작업해야할 것
- 값 중복을 핉터링하기위해 serializer.py에서 ```UniqueTogetherValidator``` 옵션을 통해 중복값 들어가지 않도록 설정해놓은 상태, 하지만 ```daily_process.py``` 실행에서 중복값 발생시 어떻게 처리할지 결정해야함
- 현재 : 중복 발생 or is_valid 시  count += , 최종 save() 끝날 시  count 출력하여 not is_valid() 개수 출력



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


