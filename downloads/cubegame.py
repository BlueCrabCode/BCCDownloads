from __future__ import annotations

class display:
    def getwin(size: (int, int) = (500, 500), title: str = 'cubegame | v1.0.0'):
        from tkinter import Tk, Canvas

        tkwin = Tk()
        tkwin.title(title)
        tkwin.geometry('{}x{}'.format(size[0], size[1]))
        tkwin.canvas = Canvas(tkwin, bg='black', width=size[0], height=size[1])
        tkwin.canvas.pack()
        tkwin.campos = (0, 0)
        tkwin.update_idletasks()
        tkwin._window = display._window()

        return tkwin._window

    def convertrgb(color: (int, int, int)) -> str:
        return '#%02x%02x%02x' % color

    class _window:
        def fill(self, color):
            from tkinter import _default_root
            canvas = _default_root.canvas
            canvas.delete('all')
            w = int(canvas['width'])
            h = int(canvas['height'])
            canvas.create_rectangle(0, 0, w, h, fill=display.convertrgb(color), outline='')

        def render(self, sprite: sprites.rect | sprites.text):
            from tkinter import _default_root
            canvas = _default_root.canvas
            camx, camy = _default_root.campos

            if (type(sprite) == sprites.rect):
                x, y = sprite.pos
                w, h = sprite.size
                color = display.convertrgb(sprite.color)
                canvas.create_rectangle(x - camx, y - camy, x + w - camx, y + h - camy, fill=color, outline='')
            elif (type(sprite) == sprites.text):
                x, y = sprite.pos
                color = display.convertrgb(sprite.color)
                canvas.create_text(x - camx, y - camy, text=sprite.text, fill=color, font=('Arial', sprite.size))

        def destroy(self):
            from tkinter import _default_root
            _default_root.destroy()


class sprites:
    class _sprite:
        def __init__(self):
            self.pos = (0, 0)
            self.color = (0, 0, 0)

        def changePosX(self, x: int, increase: bool = False):
            self.pos = (self.pos[0] + x if increase else x, self.pos[1])

        def changePosY(self, y: int, increase: bool = False):
            self.pos = (self.pos[0], self.pos[1] + y if increase else y)

        def changeColorR(self, r: int, increase: bool = False):
            self.color = (self.color[0] + r if increase else r, self.color[1], self.color[2])

        def changeColorG(self, g: int, increase: bool = False):
            self.color = (self.color[0], self.color[1] + g if increase else g, self.color[2])

        def changeColorB(self, b: int, increase: bool = False):
            self.color = (self.color[0], self.color[1], self.color[2] + b if increase else b)

    class rect(_sprite):
        def __init__(self, pos: (int, int) = (0, 0), size: (int, int) = (0, 0), color: (int, int, int) = (0, 0, 0)):
            super().__init__()
            self.pos = pos
            self.size = size
            self.color = color

        def changeSizeW(self, w: int, increase: bool = False):
            self.size = (self.size[0] + w if increase else w, self.size[1])

        def changeSizeH(self, h: int, increase: bool = False):
            self.size = (self.size[0], self.size[1] + h if increase else h)

        def collision(self, other):
            ax1, ay1 = self.pos
            ax2, ay2 = ax1 + self.size[0], ay1 + self.size[1]

            bx1, by1 = other.pos
            bx2, by2 = bx1 + other.size[0], by1 + other.size[1]

            return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

    class text(_sprite):
        def __init__(self, pos: (int, int) = (0, 0), text: str = '', size: int = 12, color: (int, int, int) = (0, 0, 0)):
            super().__init__()
            self.pos = pos
            self.text = text
            self.color = color
            self.size = size

class controller:
    _keys = {}
    _mousepos = (0, 0)
    _mousedelta = (0, 0)
    _mousedown = False

    def init():
        from tkinter import _default_root
        _default_root.bind('<KeyPress>', controller._key_press)
        _default_root.bind('<KeyRelease>', controller._key_release)
        _default_root.bind('<Motion>', controller._mouse_move)
        _default_root.bind('<ButtonPress-1>', controller._mouse_down)
        _default_root.bind('<ButtonRelease-1>', controller._mouse_up)
        return controller

    def getkey(key: chr | str) -> bool:
        return controller._keys.get(key, False)

    def getmousepos() -> (int, int):
        return controller._mousepos

    def getmousedelta() -> (int, int):
        return controller._mousedelta

    def getmousedown() -> bool:
        return controller._mousedown

    def _key_press(event):
        controller._keys[event.keysym] = True

    def _key_release(event):
        controller._keys[event.keysym] = False

    def _mouse_move(event):
        controller._mousedelta = (event.x - controller._mousepos[0], event.y - controller._mousepos[1])
        controller._mousepos = (event.x, event.y)

    def _mouse_down(event):
        controller._mousedown = True

    def _mouse_up(event):
        controller._mousedown = False

class draw:
    def rect(pos: (int,int), size: (int,int), color: (int,int,int)=(0,0,0), outline=None, width=1):
        from tkinter import _default_root
        win = _default_root._window
        sprite = sprites.rect(pos, size, color)
        win.render(sprite)

    def text(pos: (int,int), text: str, size=12, color=(0,0,0), font='Arial', bold=False):
        from tkinter import _default_root
        win = _default_root._window
        sprite = sprites.text(pos, text, size, color)
        win.render(sprite)

    def line(start: (int,int), end: (int,int), width=1, color=(0,0,0)):
        from tkinter import _default_root
        from math import atan2
        win = _default_root._window

        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        length = (dx*dx + dy*dy)**0.5
        angle = atan2(dy, dx)

        rect_pos = (x1, y1 - width/2)
        rect_size = (length, width)
        sprite = sprites.rect(rect_pos, rect_size, color)
        win.render(sprite)

class time:
    def after(ms: int, func: callable):
        from tkinter import _default_root
        _default_root.after(ms, func)


def run():
    from tkinter import _default_root
    _default_root.mainloop()
