#!/usr/bin/env python3

from logging import getLogger
from logging.config import dictConfig
from sys import argv

from flask import Flask, redirect
from pytube import YouTube as _YouTube


class YouTube(_YouTube):
    def __init__(self, vid):
        super().__init__(f'https://youtube.com/{vid}')

    @property
    def hls_manifest_url(self):
        """Return hlsManifestUrl from video info."""
        return self.streaming_data['hlsManifestUrl']


level = 'DEBUG' if '--debug' in argv else 'INFO'
dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s.%(msecs)03d %(levelname)-5s %(name)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': level,
                'formatter': 'simple',
            }
        },
        'root': {'level': level, 'handlers': ('console',)},
        'loggers': {'urllib3.connectionpool': {'level': 'INFO'}},
    }
)


def create_app():
    app = Flask('sonos-youtube')

    log = getLogger()

    @app.route('/<string:vid>')
    def youtube(vid):
        yt = YouTube(vid)
        url = yt.hls_manifest_url
        log.info('vid=%s -> url=%s', vid, url)
        return redirect(url, code=302)

    log.info('Example URL: http://<host-fqdn>:<port>/jfKfPfyJRdk')
    return app
