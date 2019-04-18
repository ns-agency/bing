## Drive.bing

To run this site first you must install docker, then you can do

```
$ cd drive.bing
$ docker-compose build
```

This command will take a while the first time you run it, but will take significantly less time in subsequent runs. 

Once the stack has been built you can launch it via the `up` command and take it down via the `down` command. Note that you can give the up command the argument `-d` to leave the site running in the background. 

```
$ docker-compose up -d
```

Everytime you make a change to the code you will need to rebuild the image and relaunch it 

```
$ docker-compose build
$ docker-compose up -d
```

You may find it useful to not detach from the process so you can see live logs of the site.

```
$ docker-compose build
$ docker-compose up
```

Once the site is running you can visit it at `localhost:8010`

Once it is up you can run a set of tests via
```
$ cd drive.bing
# .. source into a virtual env if you want to (optional)
$ pip install -r test_requirements.txt
$ python3 tests.py
```

Replace the global host variable in the source code if you are running the tests on a different machine from where the image is running.

## Pastebing

To run this site first you must install docker, then you can do

```
$ cd pastebing
$ docker-compose build
```

This command will take a while the first time you run it, but will take significantly less time in subsequent runs.

Once the stack has been built you can launch it via the `up` command and take it down via the `down` command. Note that you can give the up command the argument `-d` to leave the site running in the background. 

```
$ docker-compose up -d
```

Everytime you make a change to the code you will need to rebuild the image and relaunch it 

```
$ docker-compose build
$ docker-compose up -d
```

You may find it useful to not detach from the process so you can see live logs of the site.

```
$ docker-compose build
$ docker-compose up
```

Once the site is running you can visit it at `localhost:8009`

Once it is up you can run a set of tests via
```
$ cd pastebing
# .. source into a virtual env if you want to (optional)
$ pip install -r test_requirements.txt
$ python3 tests.py
```

Replace the global host variable in the source code if you are running the tests on a different machine from where the image is running.