"""Drive Football Manager from the outside: screenshots, clicks, keys.

usage:
  fmctl.py shot [out.png] [--scale 0.5]   focus FM, capture its window
  fmctl.py click X Y [--right|--double]   click at window-relative coords (full-res frame)
  fmctl.py move X Y
  fmctl.py scroll X Y N                   N>0 up, N<0 down
  fmctl.py key KEY [KEY...]               e.g. esc, enter, ctrl+s
  fmctl.py type TEXT
  fmctl.py info                           window rect
"""
import ctypes, sys, time
from ctypes import wintypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)
import mss, pyautogui
from PIL import Image

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05
user32 = ctypes.windll.user32


def find_fm():
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(h, _):
        if not user32.IsWindowVisible(h):
            return True
        n = user32.GetWindowTextLengthW(h)
        buf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(h, buf, n + 1)
        cls = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(h, cls, 256)
        if buf.value.startswith("Football Manager") or (cls.value == "UnityWndClass" and buf.value):
            found.append(h)
        return True

    user32.EnumWindows(cb, 0)
    if not found:
        sys.exit("FM window not found")
    return found[0]


def client_rect(h):
    r = wintypes.RECT()
    user32.GetClientRect(h, ctypes.byref(r))
    pt = wintypes.POINT(0, 0)
    user32.ClientToScreen(h, ctypes.byref(pt))
    return pt.x, pt.y, r.right, r.bottom


def focus(h):
    if user32.IsIconic(h):
        user32.ShowWindow(h, 9)
    # Alt tap lets SetForegroundWindow succeed from a background process
    user32.keybd_event(0x12, 0, 0, 0)
    user32.SetForegroundWindow(h)
    user32.keybd_event(0x12, 0, 2, 0)
    time.sleep(0.4)


def main(a):
    h = find_fm()
    x0, y0, w, hgt = client_rect(h)
    cmd = a[0]
    if cmd == "info":
        print(x0, y0, w, hgt)
        return
    focus(h)
    if cmd == "shot":
        out = a[1] if len(a) > 1 and not a[1].startswith("--") else "fm.png"
        scale = float(a[a.index("--scale") + 1]) if "--scale" in a else 1.0
        with mss.MSS() as s:
            g = s.grab({"left": x0, "top": y0, "width": w, "height": hgt})
        img = Image.frombytes("RGB", g.size, g.rgb)
        if scale != 1.0:
            img = img.resize((int(w * scale), int(hgt * scale)), Image.LANCZOS)
        img.save(out)
        print(out, img.size)
    elif cmd in ("click", "move", "scroll"):
        x, y = x0 + int(a[1]), y0 + int(a[2])
        pyautogui.moveTo(x, y, duration=0.15)
        if cmd == "click":
            pyautogui.click(button="right" if "--right" in a else "left", clicks=2 if "--double" in a else 1)
        elif cmd == "scroll":
            pyautogui.scroll(int(a[3]) * 120)
    elif cmd == "key":
        for k in a[1:]:
            pyautogui.hotkey(*k.split("+"))
            time.sleep(0.15)
    elif cmd == "type":
        pyautogui.write(" ".join(a[1:]), interval=0.03)
    time.sleep(0.3)


if __name__ == "__main__":
    main(sys.argv[1:] or ["info"])
