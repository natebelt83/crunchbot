# steem setup

### homebrew
My best guess is that the openssl program is there, but the source files that Steem needs are not. To get those added, we can use another package manager called Homebrew. This is similar to how pip works for python but geared towards the mac operating system.

Details are here: https://brew.sh/  I believe you just need to run that main command from the Terminal:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### openssl
You can use homebrew to add openssl:
```
brew install openssl
```

Then reset those two variables to find the openssl files:
```
export CFLAGS="-I$(brew --prefix openssl)/include $CFLAGS"
export LDFLAGS="-L$(brew --prefix openssl)/lib $LDFLAGS"
```

And then hopefully the Steem install will work:
```
pip3 install steem
```
