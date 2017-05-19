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

        # Widgets

            # -Prompt Button
        self.promptBtn = Gtk.Button(label="Choose folder")
        self.promptBtn.set_size_request(200,100)
        self.promptBtn.connect("clicked", self.promptFolder)
        self.box1.pack_start(self.promptBtn, True, False, 0)

            # -Output Button
        self.outputBtn = Gtk.Button(label="Choose output")
        self.outputBtn.set_sensitive(False)
        self.outputBtn.set_size_request(200,100)
        self.outputBtn.connect("clicked", self.promptOutput)
        self.box1.pack_start(self.outputBtn, True, False, 0)

            # -Folder label
        self.folderLabel = Gtk.Label("Nothing selected...")
        self.box0.pack_start(self.folderLabel, True, False, 0)

            # -File Chooser
        self.chooser = Gtk.FileChooserDialog(title=None,action=Gtk.FileChooserAction.SELECT_FOLDER,
                                  buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))

            # -File Saver
        self.saveDialog = Gtk.FileChooserDialog(title=None,action=Gtk.FileChooserAction.SAVE,
                                  buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE,Gtk.ResponseType.OK))

        self.promptBtn.show()
        self.folderLabel.show()

        self.window.add(self.box0)
        self.box0.show()
        self.window.set_title("Solus Package Creator")
        self.window.resize(600, 400)
        self.window.show_all()
        self.window.connect("delete-event", self.destroy)
        Gtk.main()

    def promptFolder(self, btn=None, recurse=False):
        if recurse == False:
            self.chooser = Gtk.FileChooserDialog(title=None,action=Gtk.FileChooserAction.SELECT_FOLDER,
                                      buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
        response = self.chooser.run()
        if response == Gtk.ResponseType.OK:
            self.path = self.chooser.get_filename()
            if os.path.isfile(self.path + '/settings.json'):
                self.chooser.destroy()
                self.outputBtn.set_sensitive(True)
                self.folderLabel.set_label(self.path)
            else:
                message = Gtk.MessageDialog(parent=None,
                            flags=0,
                            type=Gtk.MessageType.ERROR,
                            buttons=(Gtk.STOCK_OK, Gtk.ResponseType.OK))
                message.set_markup("No configuration file detected within directory.")
                response = message.run()
                if response == Gtk.ResponseType.OK:
                    message.destroy()
                    # self.chooser.destroy()
                    self.promptFolder(recurse=True)
        elif response == Gtk.ResponseType.CANCEL:
            print('No folder selected')
            self.chooser.destroy()

    def createSaveDialog(self):
        self.saveDialog = Gtk.FileChooserDialog(title=None,action=Gtk.FileChooserAction.SAVE,
                                  buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
        filter = Gtk.FileFilter()
        filter.set_name("Solus Package")
        filter.add_pattern("*.sol")
        self.saveDialog.add_filter(filter)

    def promptOutput(self, btn=None, recurse=False):
        if recurse == False:
            self.createSaveDialog()
        response = self.saveDialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = self.saveDialog.get_filename()
            if not self.filename[-4:] == '.sol':
                self.filename += '.sol'
            createPkg(self.filename, self.path)
        self.saveDialog.destroy()
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
