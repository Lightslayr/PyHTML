
import pyglet as pg
from parser import Node
window = pg.window.Window(width=800, height=600, caption="PyHtml")

def render(root: Node):
    print("do somethings")
default_stylesheet = {
    "div": {
        "display":"block",
    },
    "html": {
        "display":"block",
    },
    "head": {
        "display":"none",
    },
    "meta": {
        "display":"none",
    },
    "title": {
        "display":"none",
    },
    "link": {
        "display":"none",
    },
    "style": {
        "display":"none",
    },
    "script": {
        "display":"none",
    },
    "body": {
        "display":"none",
    }

}
