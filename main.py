from zipfile import ZipFile
import pygtk
pygtk.require('2.0')
import gtk
import json
import os

class Base:
    def destroy(self, widget, data=None):
        print("Program closed.")
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        self.chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = self.chooser.run()
        if response == gtk.RESPONSE_OK:
            self.path = self.chooser.get_filename()
            if os.path.isfile(self.path + '/settings.json'):
                print 'JSON exists'
            else:
                print 'No JSON present'
        elif response == gtk.RESPONSE_CANCEL:
            print 'No folder selected'
        self.chooser.destroy()
        fixed = gtk.Fixed()
        # fixed.put(self.chooser, 50, 50)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()

dict = {
    'executable': 'Popcorn-Time',
    'icon': 'src/app/icon.png',
    'name': 'Popcorn Time'
}

data = json.dumps(dict)

with ZipFile('test-pt.sol', 'w') as pkg:
    pkg.writestr('setting.json', data)
