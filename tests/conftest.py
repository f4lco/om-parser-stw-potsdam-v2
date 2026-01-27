import datetime as _dt

import httpretty.core as _httpretty_core


class _PatchedDateTime(_dt.datetime):
    @classmethod
    def utcnow(cls):
        return _dt.datetime.now(_dt.UTC)


def pytest_configure():
    _httpretty_core.datetime = _PatchedDateTime
