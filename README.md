#Watch Face: Selfie Time

A webapp that turns a photo into an analog Pebble watchface.

The server accepts image uploads, resizes and decolors the image and places is into the resources of a Pebble project. It runs the pebble compiler, and serves back the binary.

![](https://raw.githubusercontent.com/revan/watchface/master/screenshot.png)

The server has python dependencies, listed in `requirements.txt`. `Pillow` also depends on some system packages, notably the `jpeg` and `zip` dev libraries.
