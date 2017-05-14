from zipfile import ZipFile
import pygtk
pygtk.require('2.0')
import gtk
import json
import os

class Base:
    def destroy(self, widget, data=None):
        gtk.main_quit()
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        # Boxes
        self.box0 = gtk.VBox()
        self.box1 = gtk.HBox()
        self.box0.pack_start(self.box1, fill=False)

        # Widgets

            # -Prompt Button
        self.promptBtn = gtk.Button(label="Choose folder")
        self.promptBtn.set_size_request(200,100)
        self.promptBtn.connect("clicked", self.promptFolder)
        self.box1.pack_start(self.promptBtn, fill=False)

            # -Output Button
        self.outputBtn = gtk.Button(label="Choose output")
        self.outputBtn.set_sensitive(False)
        self.outputBtn.set_size_request(200,100)
        self.outputBtn.connect("clicked", self.promptOutput)
        self.box1.pack_start(self.outputBtn, fill=False)

            # -Folder label
        self.folderLabel = gtk.Label("Nothing selected...")
        self.box0.pack_start(self.folderLabel, fill=False)

            # -File Chooser
        self.chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))

            # -File Saver
        self.saveDialog = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))

        self.promptBtn.show()
        self.folderLabel.show()

        self.window.add(self.box0)
        self.box0.show()
        self.window.set_title("Solus Package Creator")
        self.window.resize(600, 400)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)
    def promptFolder(self, btn=None, recurse=False):
        if recurse == False:
            self.chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                          buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        response = self.chooser.run()
        if response == gtk.RESPONSE_OK:
            self.path = self.chooser.get_filename()
            if os.path.isfile(self.path + '/settings.json'):
                self.chooser.destroy()
                self.outputBtn.set_sensitive(True)
                self.folderLabel.set_label(self.path)
            else:
                message = gtk.MessageDialog(parent=None,
                            flags=0,
                            type=gtk.MESSAGE_ERROR,
                            buttons=gtk.BUTTONS_OK,
                            message_format=None)
                message.set_markup("No configuration file detected within directory.")
                response = message.run()
                if response == gtk.RESPONSE_OK:
                    message.destroy()
                    # self.chooser.destroy()
                    self.promptFolder(recurse=True)
        elif response == gtk.RESPONSE_CANCEL:
            print 'No folder selected'
            self.chooser.destroy()
    def createSaveDialog(self):
        self.saveDialog = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        filter = gtk.FileFilter()
        filter.set_name("Solus Package")
        filter.add_pattern("*.sol")
        self.saveDialog.add_filter(filter)
    def promptOutput(self, btn=None, recurse=False):
        if recurse == False:
            self.createSaveDialog()
        response = self.saveDialog.run()
        if response == gtk.RESPONSE_OK:
            self.filename = self.saveDialog.get_filename()
            if not self.filename[-4:] == '.sol':
                self.filename += '.sol'
            createPkg(self.filename, self.path)
        elif response == gtk.RESPONSE_CANCEL:
            print 'No folder selected'
        self.saveDialog.destroy()
    def main(self):
        gtk.main()

def createPkg(filename, folder):
    with ZipFile(filename, 'w') as pkg:
        for dirname, subdirs, files in os.walk(folder):
            print dirname
            print 'sub'
            print subdirs
            print 'fi'
            print files
            relDir = os.path.relpath(dirname, folder)
            pkg.write(dirname, relDir)
            for file in files:
                pkg.write(os.path.join(dirname, file), os.path.join(relDir, file))

        # pkg.writestr('setting.json', data)

if __name__ == "__main__":
    base = Base()
    base.main()
