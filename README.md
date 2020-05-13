# os-scrapy-ipfilter-resolver

[![Build Status](https://www.travis-ci.org/cfhamlet/os-scrapy-ipfilter-resolver.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-scrapy-ipfilter-resolver)
[![codecov](https://codecov.io/gh/cfhamlet/os-scrapy-ipfilter-resolver/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-scrapy-ipfilter-resolver)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-scrapy-ipfilter-resolver.svg)](https://pypi.python.org/pypi/os-scrapy-ipfilter-resolver)
[![PyPI](https://img.shields.io/pypi/v/os-scrapy-ipfilter-resolver.svg)](https://pypi.python.org/pypi/os-scrapy-ipfilter-resolver)

This project provide a DNS Resolver for ip blacklist/whitelist and config DNS expire time.

## Install

```
pip install os-scrapy-ipfilter-resolver
```

You can run example spider directly in the project root path.

```
scrapy crawl example
```

## Usage

### Settings

* enable DNS Resolver, in the project settings.py file:

    ```
    DNS_RESOLVER = "os_scrapy_ipfilter_resolver.Resolver"
    ```

* config IP blacklist, it will raise ``IPFilteredException`` when the request ip in the blacklist

    ```
    IP_DISALLOWED = ["192.168.0.0/16", "10.143.0.1"]
    ```

* config IP whitelist, priority greater than blacklist

    ```
    IP_ALLOWED = ["192.168.0.1"]
    ```

* config DNS cache size and expire time(seconds)

    ```
    DNSCACHE_ENABLED = True
    DNSCACHE_SIZE = 10000
    DNSCACHE_EXPIRE = 24 * 60 * 60
    ```

* config DNS lookup timeout(seconds)

    ```
    DNS_TIMEOUT = 60
    ```

## Unit Tests

```
tox
```

## License

MIT licensed.
