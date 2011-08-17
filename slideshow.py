#!/usr/bin/env python

import clutter
import os
import gobject

image_dir = 'images'
interval = 2000
maxium = 5
width = 1024
height = 768

class Slideshow:
    def __init__(self):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.Color(0,0,0,255))
        self.files = sorted(os.listdir(image_dir))
        if len(self.files) > maxium:
            self.files = self.files[maxium*-1:]
        self.load_files()
        self.texture = None
        self.previous = None
        self.stage.show()
        self.stage.connect('destroy', clutter.main_quit)
        

    def start(self):
        self.stage.set_width(width)
        self.stage.set_height(height)
        self.stage.set_fullscreen(True)
        self.load_files()
        self.play(None, pos=len(self.files)-1)

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
        last = self.files[len(self.files)-1]
        files = sorted(os.listdir(image_dir), reverse=True)

        if len(files) > 0 and files[0] != last:
            tmp = []
            for f in files:
                if f != last:
                    tmp.insert(0, f)
                else:
                    break;
            self.files = self.files + tmp
            if len(self.files) > maxium:
                self.files = self.files[maxium*-1:]
            for f in tmp:
                self.load_file(f)
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
        self.imageviews.append(texture)
    
    def load_files(self):
        self.imageviews = []
        for f in self.files:
            self.load_file(f)

    def play(self, animation, pos=0):
        ret = self.append_files()
        if pos < 0 or ret:
            pos = len(self.files)-1

        self.pos = pos
        if self.texture != None:
            self.previous = self.texture
            self.previous.detach_animation()
            anim = self.previous.animate (clutter.LINEAR, interval, "opacity", 0)
            anim.connect('completed', self.remove_texture, self.previous)

        print "total: %s, current: %s" % (len(self.files), pos)
        self.texture = self.imageviews[pos]
        self.stage.add(self.texture)
        anim = self.texture.animate (clutter.LINEAR, interval, "opacity", 255)
        anim.connect('completed', self.play, pos-1)

    def remove_texture(self, animation, actor):
        actor.get_parent().remove(actor)

def main():
    slideshow = Slideshow()
    gobject.timeout_add(10, slideshow.start)
    clutter.main()

if __name__ == '__main__':
    main()
