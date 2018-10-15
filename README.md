# OpenMensa Parser STW Potsdam

[![Build Status](https://travis-ci.org/f4lco/om-parser-stw-potsdam-v2.svg?branch=master)](https://travis-ci.org/f4lco/om-parser-stw-potsdam-v2)
[![Coverage Status](https://coveralls.io/repos/github/f4lco/om-parser-stw-potsdam-v2/badge.svg?branch=master)](https://coveralls.io/github/f4lco/om-parser-stw-potsdam-v2?branch=master)
[![Read the Docs](https://readthedocs.org/projects/om-parser-stw-potsdam-v2/badge/?version=latest&style=flat)](https://om-parser-stw-potsdam-v2.readthedocs.io/en/latest/)

[OpenMensa][om] parser components query canteen websites for menus and transform them into OpenMensa's data format.
This project came to life after the website of the canteens of the Studentenwerk Potsdam changed, and is therefore the successor to [kaifabian/om-parser-potsdam][prev-parser] (hence the "-v2").

Among others, OpenMensa powers the popular [Mensa Uni Potsdam][steppschuh] Android app.

The current application is built with [Python][py], [PyOpenMensa][pom], and [Flask][flask]. Learn more about the technical details at [Read the Docs][rtd].

**Contributions** are always welcome, in particular if the response format of the canteens change. Feel free to file a PR with improvements.

**Deployment** If in need of a deployment, file a PR to this fork: [kaifabian/om-parser-potsdam-v2](kai). Kai is currently in charge of running an instance of the parser and the registration on the OpenMensa platform.

**Where to go next** maybe use this parser or the OpenMensa API to source a new dataset for training a predictor for your favorite lunch?

**License** Just assume this project is licensed in terms of [WTFPL](http://www.wtfpl.net/) ;)

[om]: https://openmensa.org
[prev-parser]: https://github.com/kaifabian/om-parser-potsdam
[rtd]: https://om-parser-stw-potsdam-v2.readthedocs.io/en/latest/
[steppschuh]: https://steppschuh.net/blog/?p=951
[py]: http://python.org
[pom]: https://github.com/mswart/pyopenmensa
[flask]: https://palletsprojects.com/p/flask/
[kai]: https://github.com/kaifabian/om-parser-stw-potsdam-v2