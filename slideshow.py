#!/usr/bin/env python

import clutter
import os

image_dir = 'images'
interval = 2000
maxium = 5

class Slideshow:
    def __init__(self):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.Color(0,0,0,255))
        self.files = sorted(os.listdir(image_dir))
        print self.files
        if len(self.files) > maxium:
            self.files = self.files[maxium*-1:]
        print self.files
        self.load_files()
        self.texture = None
        self.previous = None
        self.stage.show()
        self.stage.connect('destroy', clutter.main_quit)

    def get_scale(self, actor):
        method = None
        ratio = 0.9
        if actor.get_width() > actor.get_height():
            method = "get_width"
        else:
            method = "get_height"

        ds = getattr(self.stage, method)()
        da = getattr(actor, method)()
        return ds*ratio/da

    def destroy_remain(self):
        if len(self.imageviews) < maxium:
            return;

        views = self.imageviews[maxium:]
        for v in views:
            self.imageviews.remove(v)
            v.destroy()

    def append_files(self):
        files = sorted(os.listdir(image_dir), reverse=True)
        if len(files) > 0 and files[0] != self.files[0]:
            for f in files:
                if f != self.files[0]:
                    self.files.insert(0, f)
                else:
                    break;
            self.destroy_remain()
            return True
        else:
            return False

    def load_file(self, f):
        texture = clutter.Texture("%s/%s" % (image_dir, f))
        texture.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
        texture.set_x(self.stage.get_width()/2)
        texture.set_y(self.stage.get_height()/2)
        scale = self.get_scale(texture)
        texture.set_scale(scale, scale)
        texture.set_opacity(0)
        self.imageviews.insert(0, texture)
    
    def load_files(self):
        self.imageviews = []
        for f in self.files:
            self.load_file(f)

    def play(self, animation, pos=0):
        if pos >= len(self.imageviews):
            pos = 0
        self.pos = pos
        if self.texture != None:
            self.previous = self.texture
            self.previous.detach_animation()
            anim = self.previous.animate (clutter.LINEAR, interval, "opacity", 0)
            anim.connect('completed', self.destroy_texture, self.previous)

        print "total: %s, current: %s" % (len(self.files), pos)
        self.texture = self.imageviews[pos]
        self.stage.add(self.texture)
        anim = self.texture.animate (clutter.LINEAR, interval, "opacity", 255)
        anim.connect('completed', self.play, pos+1)

    def destroy_texture(self, animation, actor):
        actor.get_parent().remove(actor)

def main():
    slideshow = Slideshow()
    slideshow.load_files()
    slideshow.play(None, pos=0)
    clutter.main()

if __name__ == '__main__':
    main()
