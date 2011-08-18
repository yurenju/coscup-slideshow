#!/usr/bin/env python

import clutter
import os
import gobject

image_dir = 'images'
interval = 5000
maxium = 50
width = 1024
height = 768

class Slideshow:
    def __init__(self):
        self.stage = clutter.Stage()
        self.stage.set_color(clutter.Color(0,0,0,255))
        
        self.files = []
        files = sorted(os.listdir(image_dir))
        for f in files:
            item = {}
            item['filename'] = f
            item['texture'] = None
            self.files.append(item)
            
        if len(self.files) > maxium:
            self.files = self.files[maxium*-1:]

        self.current = None
        self.previous = None
        self.stage.show()
        self.stage.connect('destroy', clutter.main_quit)

    def start(self):
        self.stage.set_width(width)
        self.stage.set_height(height)
        self.stage.set_fullscreen(True)
        self.load_files()
        self.play(None)

    def get_scale(self, actor):
        method = None
        ratio = 0.9
        if actor.get_width() > actor.get_height():
            method = "get_width"
        else:
            method = "get_height"

        ds = getattr(self.stage, method)()
        da = getattr(actor, method)()
        
        if da == 0:
            return 0
        return ds*ratio/da

    def destroy_remain(self):
        if len(self.files) < maxium:
            return;
            
        for item in self.files[:maxium*-1]:
            if item['texture'] != None:
                item['texture'].destroy()
        del self.files[:maxium*-1]

    def append_files(self):
        last = self.files[-1]
        files = sorted(os.listdir(image_dir))

        if len(files) > 0 and files[-1] != last['filename']:
            i = files.index(last['filename'])
            for f in files[i+1:]:
                item = {}
                item['filename'] = f
                item['texture'] = self.load_file(item['filename'])
                self.files.append(item)
                
            self.destroy_remain()
            return True
        else:
            return False

    def load_file(self, filename):
        texture = clutter.Texture("%s/%s" % (image_dir, filename))
        texture.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
        texture.set_x(self.stage.get_width()/2)
        texture.set_y(self.stage.get_height()/2)
        scale = self.get_scale(texture)
        texture.set_scale(scale, scale)
        texture.set_opacity(0)
        return texture
    
    def load_files(self):
        for f in self.files:
            f['texture'] = self.load_file(f['filename'])

    def get_index(self, f):
        return self.files.index(f)

    def play(self, animation):
        ret = self.append_files()
        if self.current != None:
            self.previous = self.current
            self.previous['texture'].detach_animation()
            anim = self.previous['texture'].animate (clutter.LINEAR, interval, "opacity", 0)
            anim.connect('completed', self.remove_texture, self.previous['texture'])

        if self.current == None or ret or self.get_index(self.current) < 1:
            self.current = self.files[-1]
        else:
            index = self.get_index(self.current)
            self.current = self.files[index-1]

        print "(%s/%s) - %s" % (self.files.index(self.current), \
                len(self.files), self.current['filename'])

        self.stage.add(self.current['texture'])
        anim = self.current['texture'].animate (clutter.LINEAR, interval, "opacity", 255)
        anim.connect('completed', self.play)

    def remove_texture(self, animation, actor):
        actor.get_parent().remove(actor)

def main():
    slideshow = Slideshow()
    gobject.timeout_add(10, slideshow.start)
    clutter.main()

if __name__ == '__main__':
    main()
