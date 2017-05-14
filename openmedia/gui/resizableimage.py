from gi.repository import Gtk, Gdk, GdkPixbuf


class ResizableImage(Gtk.EventBox):

    def __init__(self, filename):
        Gtk.EventBox.__init__(self)
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        self.image = Gtk.Image.new_from_pixbuf(self.pixbuf)
        self.add(self.image)
        self.connect('size-allocate', self.__resize_cb)


    def set_from_file(self, filename):
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        self.image.set_from_pixbuf(self.pixbuf)

    def __resize_cb(self, widget, size):
        pixbuf_new = self.pixbuf.scale_simple(size.width, size.height,
                                              GdkPixbuf.InterpType.BILINEAR)
        self.image.props.pixbuf = pixbuf_new
