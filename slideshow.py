#!/usr/bin/env python

import clutter
import os

image_dir = 'images';

class Slideshow:
    def __init__(self):
        self.stage = clutter.Stage()
        self.files = sorted(os.listdir(image_dir), reverse=True)
        self.load_files()
        self.texture = None
        self.stage.show()
    
    def load_files(self):
        self.imageviews = []
        for f in self.files:
            texture = clutter.Texture("%s/%s" % (image_dir, f))
            self.imageviews.append(texture)

    def play(self, animation, pos=0):
        if pos >= len(self.files):
            pos = 0
        self.pos = pos
        if self.texture != None:
            anim = self.texture.animate (clutter.LINEAR, 1500, "opacity", 0)
            anim.connect('completed', self.destroy_texture, self.texture)
            return

        self.texture = self.imageviews[pos]
        self.texture.set_opacity(0)
        self.texture.show()
        self.stage.add(self.texture)
        anim = self.texture.animate (clutter.LINEAR, 1500, "opacity", 255)
        anim.connect('completed', self.play, pos+1)

    def destroy_texture(self, animation, actor):
        actor.destroy()

def main():
    slideshow = Slideshow()
    slideshow.load_files()
    slideshow.play(None, pos=0)
    clutter.main()

if __name__ == '__main__':
    main()
