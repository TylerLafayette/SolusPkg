from zipfile import ZipFile
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json
import sys
import os

class Base:
    def destroy(self, widget, data=None):
        Gtk.main_quit()
        sys.exit()

    def __init__(self):
        self.window = Gtk.Window()

        # Boxes
        self.box0 = Gtk.VBox()
        self.box1 = Gtk.HBox()
        self.box0.pack_start(self.box1, False, True, 30)

            # -Select Button
        self.fileBtn = Gtk.Button(label="Select file")
        self.fileBtn.set_size_request(200,100)
        self.fileBtn.connect("clicked", self.loadFile)
        self.box1.pack_start(self.fileBtn, True, False, 0)

        self.window.set_title("Solus Package Installer")
        self.window.resize(400, 100)
        self.window.add(self.box0)
        self.box0.show()
        self.window.show_all()
        self.window.connect("delete-event", self.destroy)
        Gtk.main()
    def loadFile(self, btn=None):
        print("Loading file")
    def main(self):
        Gtk.main()

def createPkg(filename, folder):
    with ZipFile(filename, 'w') as pkg:
        for dirname, subdirs, files in os.walk(folder):
            relDir = os.path.relpath(dirname, folder)
            pkg.write(dirname, relDir)
            for file in files:
                pkg.write(os.path.join(dirname, file), os.path.join(relDir, file))

        # pkg.writestr('setting.json', data)

if __name__ == "__main__":
    base = Base()
    base.main()
