from __future__ import print_function, division
import sys
import csv

from cgkit.bvh import BVHReader
import cgkit.bvh
from joint import Joint
from skeleton import Skeleton
import logging

cgkit.bvh.Node = Joint
log = logging.getLogger("converter")

"""
Based on: http://www.dcs.shef.ac.uk/intranet/research/public/resmes/CS0111.pdf

Notes:
 - For each frame we have to recalculate from root
 - End sites are semi important (used to calculate length of the toe? vectors)
"""


class Converter(BVHReader, object):
    def __init__(self, skeleton, *args, **kwargs):
        super(Converter, self).__init__(*args, **kwargs)
        self.skeleton = skeleton
        self.count = 0

    def onHierarchy(self, root):
        self.skeleton._set_hierarchy(root)

    def onFrame(self, values):
        if self.count < 5:
            self.skeleton._add_frame(values)
            self.count += 1


def setup_logger(level):
    log.setLevel(level)

    fmt = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt="[%d/%m/%Y %H:%M]")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    stdout_handler.setLevel(level)

    fhandler = logging.FileHandler(
        filename='output.log', encoding='utf-8', mode='a')
    fhandler.setFormatter(fmt)

    log.addHandler(fhandler)
    log.addHandler(stdout_handler)


if __name__ == "__main__":
    setup_logger(logging.DEBUG)
    fname = sys.argv[1]
    print("Input filename: {}".format(fname))
    s = Skeleton()
    c = Converter(s, fname)
    c.read()
    with open("output.csv", 'w') as f:
        writer = csv.writer(f, lineterminator="\n")
        header, frames = s.frames()
        writer.writerow(header)
        for frame in frames:
            writer.writerow(frame)
    # c.dump_frames()
