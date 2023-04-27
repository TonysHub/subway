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
