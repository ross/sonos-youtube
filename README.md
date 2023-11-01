## Sonos YouTube

A trivial HTTP server to allow Sonos to play YouTube live streams.

Note: it does not currently work with non-streaming/regular videos, though it
may in the future.

### Running It

Works well running on devices like a NAS or even Raspberry PI

#### As a docker container

Recommended

```console
$ sudo ./script/update-docker
...
```

#### Stand-alone

If your setup dictates

```console
$ ./script/bootstram
$ ./script/run
```

### Using it

In the Sonos apps:

1. "Browse"
1. "TuneIn"
1. "My Radio Stations"
1. "..."
1. "Add New Radio Station"
    1. "Streaming URL"
        - Grab the ID portion of the URL you'd like to stream, in the case of `https://www.youtube.com/watch?v=jfKfPfyJRdk` that would be `jfKfPfyJRdk`
        - `http://<fqdn-or-ip-of-host-running-the-server>:9182/<id-from-above>`, e.g. `http://my-nas.lan:9182/jfKfPfyJRdk`
    1. "Station Name"
        - Whatever you would like to call it, probably just a copy-n-paste of the stream's title
    1. "OK"

You should now be able to play the live stream on your Sonos devices. 

### How it works

One of the ways Youtube serves their videos an HLS Manifest, a `.m3u8` that happens to be supported by Sonos. However these URLs change over time so you can't just stick one into the "Streaming URL" field of a Sonos radio station. This simple server fetches the current data for the video and thend does a 302 redirect to the current URL. That's it.
