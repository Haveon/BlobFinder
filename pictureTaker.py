from subprocess import call
from argparse import ArgumentParser

def capture(fname, videoDevice='/dev/video1', resolution='1000x1000'):
    call(['fswebcam', '-d', videoDevice, '-r', resolution, '--jpeg', '85', '--no-banner', fname])
    return

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('fname', help='filename and path you wish to save to')
    parser.add_argument('-d', '--device', default='/dev/video1', help='Path to image capture device')
    parser.add_argument('-r', '--resolution', default='1920x1080', help='Image resolution in pixels')
    args = parser.parse_args()
    capture(args.fname, args.device, args.resolution)