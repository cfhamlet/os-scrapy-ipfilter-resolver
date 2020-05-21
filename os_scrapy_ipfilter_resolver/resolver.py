import logging

from expiringdict import ExpiringDict
from IPy import IP, IPSet
from scrapy.resolver import dnscache
from twisted.internet import defer
from twisted.internet.base import ThreadedResolver


class IPFilteredException(Exception):
    pass


class Resolver(ThreadedResolver):
    def __init__(
        self, reactor, cache_size, cache_expire, timeout, disallowed=None, allowed=None
    ):
        super(Resolver, self).__init__(reactor)
        self.disallowed = IPSet(
            [IP(ip) for ip in (disallowed if disallowed is not None else [])]
        )
        self.allowed = IPSet(
            [IP(ip) for ip in (allowed if allowed is not None else [])]
        )

        self.cache_allowed = self.cache_disallowed = None
        if cache_size > 0:
            self.cache_allowed = ExpiringDict(
                max_len=cache_size, max_age_seconds=cache_expire
            )
            self.cache_disallowed = ExpiringDict(
                max_len=cache_size, max_age_seconds=cache_expire
            )

        self.timeout = timeout if isinstance(timeout, tuple) else (timeout,)
        self.logger = logging.getLogger(self.__class__.__name__)

    def getHostByName(self, name, timeout=()):
        if self.cache_allowed is not None:
            if name in self.cache_allowed:
                return defer.succeed(self.cache[name])
            elif name in self.cache_disallowed:
                result = self.cache_disallowed[name]
                raise IPFilteredException(f"ip filtered {name} {result}")
        if not timeout:
            timeout = self.timeout
        d = super(Resolver, self).getHostByName(name, timeout)
        d.addCallback(self.callback, name)
        return d

    def callback(self, result, name):
        dnscache[name] = result
        ip = IP(result)
        if ip not in self.allowed and ip in self.disallowed:
            if self.cache_disallowed is not None and name not in self.cache_disallowed:
                self.logger.warning(f"cache disallowed {name} {result}")
                self.cache_disallowed[name] = result
            raise IPFilteredException(f"ip filterd {name} {result}")
        if self.cache_allowed is not None and name not in self.cache_allowed:
            self.logger.debug(f"cache allowed {name} {result}")
            self.cache_allowed[name] = result
        return result

    def install_on_reactor(self):
        self.reactor.installResolver(self)

    @classmethod
    def from_crawler(cls, crawler, reactor):
        settings = crawler.settings
        cache_size = settings.getint("DNSCACHE_SIZE", 10000)
        cache_expire = settings.getint("DNSCACHE_EXPIRE", 24 * 60 * 60)
        timeout = settings.getfloat("DNS_TIMEOUT")
        if not settings.getbool("DNSCACHE_ENABLED"):
            cache_size = 0
        disallowed = settings.getlist("IP_DISALLOWED", [])
        allowed = settings.getlist("IP_ALLOWED", [])
        dnscache.limit = cache_size
        return cls(reactor, cache_size, cache_expire, timeout, disallowed, allowed)
