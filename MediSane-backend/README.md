# MediSane

## ❗ SETUP

Run:
```sh
pip install -r requirements.txt
```

on terminal to install required packages & modules.

Then run:
```sh
uvicorn backend.__init__:backend --reload
```
<code>--reload</code> flag enables your current changes to reflect on the app by automatically rerunning the app upon
detecting change in the code.


## ⚠️Windows
You can also add:
```sh
--no-use-colors
```

flag at the end as well if you are using Windows, as uvicorn
cannot correctly print colors on Windows terminals.

## ⚠️macOS
On macOS, you might get an error that says pymysql could not be installed.
In that case, run:

```sh
brew install python3-pymysql
```
***
> ⚠ In this step wheel can fail to build with:
> 
> 
> <code>Exception: Can not find valid pkg-config name.
>      
>
> Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually</code>
> 
To fix this:
```sh
$ brew install pkg-config
$ brew install mysql-client pkg-config
$ export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
$ pip install mysqlclient
```

***
and then rerun
```sh
pip install -r requirements.txt
```

It could be the case that mysql fails to import even when installed (this appears after you run the program).


In that case, uncomment the lines 8 & 9 in <code>db.py</code> inside callers module and follow the instructions there.

## ⌛ To be updated ⌛ 