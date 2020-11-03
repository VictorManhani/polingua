# created by Victor G. Manhani

# hide or show a widget
def hide_widget(wid, dohide=True):
    if hasattr(wid, 'saved_attrs'):
        if not dohide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif dohide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

# inheriting this class, allows the class that inherited it to be cloned.
class CloneWidget:
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		self.__dict__.update(kwargs)
		super().__init__(**kwargs)

	def copy(self):
		return self.__class__(**self.kwargs)
