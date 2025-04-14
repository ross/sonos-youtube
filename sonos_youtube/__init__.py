#!/usr/bin/env python3

from logging import getLogger
from logging.config import dictConfig
from sys import argv
from re import compile
from yaml import safe_load

from flask import Flask, redirect
from requests import Session


class YouTube:
    hls_manifest_url_re = compile(r'"hlsManifestUrl":"(?P<url>https[^"]+)"')

    def __init__(self, vid):
        self.vid = vid

    @property
    def hls_manifest_url(self):
        """Return hlsManifestUrl from video info."""
        sess = Session()

        sess.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'YSC=dbmfh1ivwpI; LOGIN_INFO=AFmmF2swRQIgVN2m02XxXpvvKC6ib2hU7pEl7VEJmE_O2F65dmkBIUcCIQDK3s4hHm480d0GHj5rQXSrNsABeyJks36eisP9hcKxTA:QUQ3MjNmd2x6MFB6akpIYTJiVnFSOG5xVGJPQlhRajNqdTVid0RYQk95YTliX0FrOUhzOWJURHdvT2gwN1Vqb3J4OEJ0ZGNWTS13dUsxbUpHbUNFem1lTzE0cVdVVDRweDg0RDRzNzBTVk16OGVsZGd0c0haT3ZHTTBSalAwWTE1eWhTR2dzdXA2SU05SDRSejlkUGFLZ0pNWnN1OC1nX2lB; _ga_5RPMD1E2GM=GS1.1.1697671036.1.0.1697671036.60.0.0; _ga=GA1.2.1316707563.1697671037; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgIQ%3D%3D; wide=1; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgIQ%3D%3D; VISITOR_INFO1_LIVE=P0iixR33mx0; HSID=AlxXhBFhUVsuo88mX; SSID=AOmO8abgg-pTIHuqQ; APISID=oIZoTynag05ZpXlC/AxyE1fVXRDWJMeNhC; SAPISID=TMdtYxaXqG55AifQ/AcelR_XJergT-ustQ; __Secure-1PAPISID=TMdtYxaXqG55AifQ/AcelR_XJergT-ustQ; __Secure-3PAPISID=TMdtYxaXqG55AifQ/AcelR_XJergT-ustQ; YTV_CLC=locsrc=1&locs=2&tz=America%2FKentucky%2FMonticello; SID=g.a000mAjVcwIwRd05g-xL6vh3wAqQL5UEoJkfXq_LecsBgnC277UHh-GlZ9S4kHMnd3jgIsXN-wACgYKAQYSARASFQHGX2MibB4lPltD3KiQzkyxCwMz5xoVAUF8yKpUVbr8STutodQStP3YN1bc0076; __Secure-1PSID=g.a000mAjVcwIwRd05g-xL6vh3wAqQL5UEoJkfXq_LecsBgnC277UHShMt27yUR5FT9ShJkUKDcgACgYKAZESARASFQHGX2MiS8rX9FP87EpSi6SRi20CuxoVAUF8yKo-lvZttjcPo9dIpzUt0c4h0076; __Secure-3PSID=g.a000mAjVcwIwRd05g-xL6vh3wAqQL5UEoJkfXq_LecsBgnC277UHx8N3X1aeskTjKBcQk6UO2AACgYKARMSARASFQHGX2MiH_eneIZrQrc1yDUmJA_g0xoVAUF8yKrM7FuQ2bASzKUmLCIAOtFZ0076; PREF=f6=80&volume=100&f7=4100&tz=America.Los_Angeles&f4=4000000&autoplay=true&f5=30000&repeat=NONE; S=youtube_lounge_remote=R5f5RJ72gP1lBhRjnNrHBN8_A001T_Lb; YT_CL={"loctok":"ACih6ZNRtu2KzLCl15sYv0JunQPkjvNgTD1n77535t2zx7pZfh9RXXzGOpX9PRMiqGrwLW2TgpGyXwFr7Z3wtUKMfyD7EqegJoc"}; __Secure-1PSIDTS=sidts-CjEB4E2dka0mCcYGGc36DLuIGNYUgNaOtrf7ThLMBMxcPW8Z7GUMSx9-oaq3AIM6A1qyEAA; __Secure-3PSIDTS=sidts-CjEB4E2dka0mCcYGGc36DLuIGNYUgNaOtrf7ThLMBMxcPW8Z7GUMSx9-oaq3AIM6A1qyEAA; SIDCC=AKEyXzVgBCflQfnU_UEZTF51AKLSIkjT_LtfmUVViHsbTPuPw405SGD_wlPoNpUnU7lN3TY7iwT7; __Secure-1PSIDCC=AKEyXzW9hZibhDe9RHUeJFQWdLvUXCQC1bIAQ_0x5UyKwqrQu3Fqm_94Yo6pfcll9ReZtNRpSV3J; __Secure-3PSIDCC=AKEyXzURfMGAbnelBgttdQNcP3gZpDruOzvX0bmL4kAL390b9cUxBNVHWcxWLtdGJwhMmYiGtA8',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-form-factors': '"Desktop"',
            'sec-ch-ua-full-version': '"126.0.6478.183"',
            'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.183", "Google Chrome";v="126.0.6478.183"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-platform-version': '"14.5.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'service-worker-navigation-preload': 'true',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-client-data': 'CJW2yQEIprbJAQipncoBCMndygEIk6HLAQiGoM0BCK2ezgEI4afOAQiKqM4BCKGuzgEI5a/OARj0yc0BGKCdzgEYxJ/OARjvp84BGLyuzgEY642lFw==',
        }
        resp = sess.get(f'https://www.youtube.com/watch?v={self.vid}')
        resp.raise_for_status()
        match = self.hls_manifest_url_re.search(resp.content.decode('utf-8'))
        if match is None:
            raise Exception('Failed to find url in html')
        return match.group('url')


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

    # Load configuration from yaml file
    with open("conf.yaml", "r") as f:
        config = safe_load(f)

    @app.route('/<string:stream_name>')  # Changed vid to stream_name
    def youtube(stream_name):  # Changed vid to stream_name
        # Get vid from config based on stream_name
        vid = config.get(stream_name)
        if not vid:
            return "Stream not found", 404
        yt = YouTube(vid)
        url = yt.hls_manifest_url
        log.info('vid=%s -> url=%s', vid, url)
        return redirect(url, code=302)

    log.info('Example URL: http://<host-fqdn>:<port>/stream1')
    return app
