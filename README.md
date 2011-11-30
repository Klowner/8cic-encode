8cic Lightwall Encoder (in python!)
===================================

A (fairly) simple utility for converting image sequences to 8cic (type 0)
media files suitable for use with the [QC-CoLab Light Wall library](https://github.com/CCDKP/QC-Co-Lab-Light-Wall).

Usage
-----

### Options
 * -i,--input -- Source image(s) (glob) or a single animated GIF.
 * -o,--output -- Destination filename (defaults to wall.dat).
 * -W,--width -- Force output width in pixels.
 * -H,--height -- Force output height in pixels.
 * -r,--repeat -- Repeat input image sequence N times (makes output file: Nx larger).
 * -d,--delay -- Inter-frame delay in milliseconds (default: 16)

### Examples

Encode an animated GIF image, repeat the animation 5 times, force 16x16 size.       

    $ 8cic_encode.py -i nyancat.gif -o nyancat.dat -r 5 -W 16 -H 16

Encode a series of PNG files named nyancat_0001.png through nyancat_0200.png, force 16x16 size, repeat 10 times, with an inter-frame delay of 24.

    $ 8cic_encode.py -i nyancat_*.png -o nyancat.dat -r 10 -d 24 -W 16 -H 16

License
-------

Apache 2.0, go read the LICENSE file

