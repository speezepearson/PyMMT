# This file defines the HistoryFrame class, basically a scrollable stack
# of labels that client code can easily add to.

from Tkinter import Label, N, S, E, W, MOVETO
from srptools.tkinter import ScrollableContainer

class HistoryFrame(ScrollableContainer):
    """A scrollable frame of labels."""
    def __init__(self, *args, **kwargs):
        ScrollableContainer.__init__(self, *args, **kwargs)
        self.labels = []

    def add(self, text):
        """Appends a new label to the bottom of the frame."""
        new_label = Label(self.content, text=text)
        new_label.grid(row=len(self.labels),
                       sticky=N+W)
        self.labels.append(new_label)
        self.reset_scrollregion()
        self.scrollable.yview(MOVETO, 1)

    def try_callback(self, callback,
                     failure_message="Error: {0.message}",
                     *args, **kwargs):
        """Attempts to return the callback. Adds a message on failure.
        
        The given message can be a format string with one positional
        argument, in which case it will be formatted with the raised
        exception. If it's not a format string or the formatting fails,
        the plain failure_message is added."""
        try:
            return callback(*args, **kwargs)
        except Exception as e:
            try:
                s = failure_message.format(e)
            except Exception as e2:
                s = failure_message
            self.add(s)
            return None
