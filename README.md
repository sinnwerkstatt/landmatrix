[comment]: <> ([![pipeline-status]&#40;https://git.sinntern.de/landmatrix/landmatrix/badges/main/pipeline.svg&#41;]&#40;https://git.sinntern.de/landmatrix/landmatrix/commits/main&#41;)
[comment]: <> ([![coverage-report]&#40;https://git.sinntern.de/landmatrix/landmatrix/badges/main/coverage.svg&#41;]&#40;https://git.sinntern.de/landmatrix/landmatrix/commits/main&#41;)

[![python version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Read the Docs](https://img.shields.io/readthedocs/landmatrix)](http://landmatrix.rtfd.io/)

# Land Matrix

The Land Matrix is a global and independent land monitoring initiative that promotes transparency and accountability in decisions over land and investment.

The website is our Global Observatory - an open tool for collecting and visualising information about large-scale land acquisitions.

Visit [https://landmatrix.org](https://landmatrix.org) for the actual database.<br>
More detailed information on the projects __structure__, __installation__ and
__development setup__ as well as a documentation of the __public API__ can be
found on [landmatrix.readthedocs.io](https://landmatrix.rtfd.io/en/latest/).

## Development

### Restore DB from file

```shell
zcat landmatrix.sql.gz | psql -h localhost -U landmatrix landmatrix
```
```shell
./manage.py migrate
```
