<a id="markdown-eyegway" name="eyegway"></a>

# Eyegway

<img src='https://img.shields.io/badge/version-0.0.1-blueviolet' /> <img src='https://img.shields.io/badge/coverage-97%25-brightgreen' /> <img src='https://img.shields.io/badge/-hatchling%20-critical' />

---

<img src="docs/images/banner.png" />

# Intro

Eyegway is a python package for data routing through `Redis` / `Dragonfly`. It is designed to be a simple and easy to use package for sending any data from a generic source to a generic destination by exploting _HUBs_(**and**)_SPOKES_ paradigm. The user can send data to a generic
_HUB_, which has a data _queue_ and a data _history_, and the data can be pulled from anywhere else. The user can implement also custom _Bridge_ to manipulate data flowing through the _HUBs_.

## Installation

```console
pip install -e .
```
