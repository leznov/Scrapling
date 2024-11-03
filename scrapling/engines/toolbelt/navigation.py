"""
Functions related to files and URLs
"""

import os
import logging
from urllib.parse import urlparse, urlencode
from playwright.sync_api import Route

from scrapling.engines.constants import DEFAULT_DISABLED_RESOURCES


def intercept_route(route: Route):
    if route.request.resource_type in DEFAULT_DISABLED_RESOURCES:
        logging.debug(f'Blocking background resource "{route.request.url}" of type "{route.request.resource_type}"')
        return route.abort()
    return route.continue_()


def construct_websocket_url(base_url, query_params):
    # Validate the base URL structure
    try:
        parsed = urlparse(base_url)

        # Check scheme
        if parsed.scheme not in ('ws', 'wss'):
            raise ValueError("URL must use 'ws://' or 'wss://' scheme")

        # Validate hostname and port
        if not parsed.netloc:
            raise ValueError("Invalid hostname")

        # Ensure path starts with /
        path = parsed.path
        if not path.startswith('/'):
            path = '/' + path

        # Reconstruct the base URL with validated parts
        validated_base = f"{parsed.scheme}://{parsed.netloc}{path}"

        # Add query parameters
        if query_params:
            query_string = urlencode(query_params)
            return f"{validated_base}?{query_string}"

        return validated_base

    except Exception as e:
        raise ValueError(f"Invalid WebSocket URL: {str(e)}")


def js_bypass_path(filename):
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, 'bypasses', filename)
