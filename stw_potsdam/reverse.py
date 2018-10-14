# -*- encoding: utf-8 -*-

import os
import urlparse

from flask import request


def reverse(path):
    override_endpoint = os.environ.get("BASE_URL", None)

    if override_endpoint:
        return urlparse.urljoin(override_endpoint, path)

    try:
        if request.url_root:
            return urlparse.urljoin(request.url_root, path)
    except RuntimeError as e:
        # outside request context, skip
        pass

    return path