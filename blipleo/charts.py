import logging
import itertools
from pyinkscape import Point, Style
from pyinkscape.styles import BLIND_COLORS


def getLogger():
    return logging.getLogger(__name__)


class Line:
    def __init__(self, pointA, pointB):
        if not pointA or not pointB or pointA == pointB:
            raise Exception(f"Invalid line points (p1={pointA}, p2={pointB})")
        self.pointA = pointA
        self.pointB = pointB

    def sig(self):
        ''' Get this line's signature in slope/intercept form '''
        if self.pointA.x == self.pointB.x:
            # vertical line
            return (None, float(self.pointA.x))
        elif self.pointA.y == self.pointB.y:
            # horizontal line
            return (0.0, float(self.pointA.y))
        else:
            slope = (self.pointA.y - self.pointB.y) / (self.pointA.x - self.pointB.x)
            intercept = self.pointB.y - slope * self.pointB.x
            return (float(slope), float(intercept))


class Quadrangle:
    def __init__(self, top, right, bottom, left):
        """

        """
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def lines(self):
        lines = []
        if self.top != self.right:
            lines.append(Line(self.top, self.right))
        if self.right != self.bottom:
            lines.append(Line(self.right, self.bottom))
        if self.bottom != self.left:
            lines.append(Line(self.bottom, self.left))
        if self.left != self.top:
            lines.append(Line(self.left, self.top))
        return lines

    def overlap(self, lines):
        for line in self.sigs():
            if line in lines:
                return True
        return False

    def sigs(self):
        ''' All signatures (slope-intercept) of lines in this quadrangle '''
        return [line.sig() for line in self.lines()]

    def __repr__(self):
        return f"Top:{self.top}-Right:{self.right}-Bottom:{self.bottom}-Left:{self.left}"

    def __add__(self, other):
        if isinstance(other, Quadrangle):
            return Quadrangle(self.top + other.top, self.right + other.right, self.bottom + other.bottom, self.left + other.left)
        else:
            return Quadrangle(self.top + other, self.right + other, self.bottom + other, self.left + other)


class SpiderChart:

    DEFAULT_LINESTYLE = Style(fill="none", stroke="#000000", stroke_miterlimit='10')

    def __init__(self, cx=50, cy=80, rx=67, ry=None, max_score=10, flex_size=2):
        self.cx = cx  # center
        self.cy = cy
        self.rx = rx  # radius x-axis
        self.ry = ry if ry else self.rx  # radius y-axis
        self.max_score = max_score
        self.flex_size = flex_size
        self._lines = set()
        self.reset_lines()

    def reset_lines(self):
        self._lines.clear()
        self._lines.add((None, self.cx))
        self._lines.add((0, self.cy))

    def graph(self):
        ''' Draw coordinate graph (vertical & horizontal) '''
        return f"M {self.cx},{self.cy-self.ry} v {self.ry * 2} M {self.cx - self.rx},{self.cy} h {self.rx * 2}"

    def line(self, c_top, c_right, c_bottom, c_left):
        ''' Create a single category path (4 points) '''
        return f"M {c_top.x},{c_top.y} L {c_right.x},{c_right.y} L {c_bottom.x},{c_bottom.y} L {c_left.x},{c_left.y} Z"

    def draw_line(self, group, top, right, bottom, left, style=None, color=None, **kwargs):
        line = self.line(top, right, bottom, left)
        _style = style if style else SpiderChart.DEFAULT_LINESTYLE.clone(stroke_width='1px')
        if color:
            _style = _style.clone(stroke=color)
        group.path(line, style=_style, **kwargs)

    def to_quadrangle(self, top, right, bottom, left):
        ''' Convert a skill matrix (i.e. scores) to drawing coordinates '''
        top_loc = Point(self.cx, self.cy - self.ry * top / self.max_score)
        right_loc = Point(self.cx + self.rx * right / self.max_score, self.cy)
        bottom_loc = Point(self.cx, self.cy + self.ry * bottom / self.max_score)
        left_loc = Point(self.cx - self.rx * left / self.max_score, self.cy)
        return Quadrangle(top_loc, right_loc, bottom_loc, left_loc)

    def shift_quads(self, quads):
        _lines = self._lines  # don't shift if not needed
        new_quads = []
        for quad in quads:
            trial = 1  # circle
            found = None if quad.overlap(_lines) else quad
            while not found:
                delta = self.flex_size * trial
                deltas = (Point(0, delta), Point(0, -delta), Point(delta, 0), Point(-delta, 0),
                          Point(delta, delta), Point(delta, -delta), Point(-delta, delta), Point(-delta, -delta))
                for d in deltas:
                    getLogger().debug(f"Trying {d}")
                    new_quad = quad + d
                    if not new_quad.overlap(_lines):
                        found = new_quad
                        break
                if not found:
                    trial += 1
            getLogger().debug(f"  shifted -> {found}")
            new_quads.append(found)
            # remember these added lines
            for line in found.lines():
                _lines.add(line.sig())
        return new_quads, _lines  # update _lines into self._lines if new_quads are drawn

    def render(self, group, scores, colors=BLIND_COLORS, id_prefix="spiderchart", **kwargs):
        # draw graph line
        group.path(self.graph(), style=SpiderChart.DEFAULT_LINESTYLE, id_prefix=f"{id_prefix}_coordinate_graph")
        self.reset_lines()
        # draw all lines
        quads = [self.to_quadrangle(top, right, bottom, left) for top, right, bottom, left in scores]
        quads, _lines = self.shift_quads(quads)
        self._lines.update(_lines)
        for idx, (quad, color) in enumerate(zip(quads, itertools.cycle(colors)), start=1):
            self.draw_line(group, quad.top, quad.right, quad.bottom, quad.left, color=color, id_prefix=f"{id_prefix}_line{idx}")
