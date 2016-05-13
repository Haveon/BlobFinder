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
    parser.add_argument('--repeat', type=int, default='1', help='How many pictures to take')
    args = parser.parse_args()
    if args.repeat!=1:
        fname,ext = args.fname.split('.')
        for i in range(args.repeat):
            raw_input('Press Enter for next picture')
            capture(fname+str(i)+'.'+ext, args.device, args.resolution)
    else:
        capture(args.fname, args.device, args.resolution)