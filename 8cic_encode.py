#!/usr/bin/env python
"""
Anything-That-PIL-Can-Read to Lightwall 8cic converter
Mark "Klowner" Riedesel (mark@klowner.com) / QCCoLab
------------------------------------------------------
version 2

Reads a series of image files (or a single animated GIF)
and converts them into lightwall ready format!

You can use a tool such as ffmpeg to convert any resize
a variety of videos available on the internets. 

example:

 $ ffmpeg -i giveyouup.flv -s 16x16 -o giveyouup_%05d.png 

Then use this script to process the resulting series of
png image files.

Requires: Python Imaging Library (PIL)

"""
import struct
import glob
import sys
from PIL import Image

FORMAT_VERSION = 3
FORMAT_TYPE = 0

def dump_color_stream(c):
    out = []
    c = [x/16 for x in c]
    for bit in reversed(range(4)):
        byte = 0
        for i, color in enumerate(c):
            byte |=  (color >> bit & 1) << i
        out.append(byte ^ 0xFF)
    return out

def process_pixel_column(pixels):
    (r,g,b) = map(lambda x:[p[x] for p in pixels], range(3))
    for color_column in (b,g,r):
        yield dump_color_stream(reversed(color_column))

def write_frame(image, size, ostream):
    (w,h) = size
    rows = h/8
    for row_groups in xrange(rows):
        for xpos in xrange(w):
            ypos = range(h)[row_groups::2]
            pixels = map(lambda y: image.getpixel((xpos,y)), ypos)
            for x in process_pixel_column(pixels):
                ostream.write(struct.pack('BBBB', *x))
    
def write_header(target_size, delay, ostream):
    (w,h) = target_size
    rows = h/8
    
    if FORMAT_VERSION > 2:
        ostream.write(struct.pack('BBBBH', FORMAT_VERSION, FORMAT_TYPE, w*rows, w, delay))
    else:
        ostream.write(struct.pack('BBB', FORMAT_VERSION, FORMAT_TYPE, w*rows))
    sys.stdout.write("HEADER [ 8cic version:%d target:%dx%d ]\n" % (FORMAT_VERSION, w,h))


def process_image_sequence(files, target_size, options, ostream):
    for x in xrange(options.repeat):
        for filename in files:
            img = Image.open(filename)
            img = img.convert('RGB')
            write_frame(img, target_size, ostream)
            sys.stdout.write("FRAME [ %s ]\n" % filename)
    

def process_animated_gif(files, target_size, options, ostream):
    filename = files[0]
    gifimg = Image.open(filename)
 
    count = 0
    while count < options.repeat:
        # REPEATEDLY INSERT FRAME TO FILL REQUEST FRAME DURATION
        for i in xrange( gifimg.info.get('duration') / options.delay):
            img = gifimg.convert('RGB')
            write_frame(img, target_size, ostream)

        try:
            gifimg.seek(gifimg.tell()+1)
        except EOFError, e:
            count += 1
            gifimg.seek(0)
            


def cmdline():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest="input_path", help="Source image(s) (glob) or single animated GIF")
    parser.add_option('-o', '--output', dest='output_file', default='wall.dat', help="Destination filename (default: wall.dat)")
    parser.add_option('-W', '--width', dest='width', default=0, type='int', help="Force width")
    parser.add_option('-H', '--height', dest='height', default=0, type='int', help="Force height")
    parser.add_option('-r', '--repeat', dest='repeat', default=1, type='int', help="Repeat N times (warning: makes file Nx larger)")
    parser.add_option('-d', '--delay', dest='delay', default=16, type='int', help="Inter-frame delay (mS, default: 16)")
    (options, args) = parser.parse_args()

    if not options.input_path:
        parser.print_help()
        return
    
    ostream = file(options.output_file, 'wb')
    files = glob.glob(options.input_path)
    files.sort()
    
    if files:
        img = Image.open(files[0])
        
        target_size = img.size
        target_size = (options.width or target_size[0], options.height or target_size[1])
        write_header(target_size, options.delay, ostream)

        if len(files) == 1 and img.format == 'GIF':
            process_animated_gif(files, target_size, options, ostream)
        else:
            process_image_sequence(files, target_size, options, ostream)

    ostream.close()
    sys.stdout.write("Done.\n")

if __name__ == '__main__':
    cmdline()

