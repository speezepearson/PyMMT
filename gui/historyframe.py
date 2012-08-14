from Tkinter import Label, N, S, E, W, MOVETO
from useful.tkinter import ScrollableContainer

class HistoryFrame(ScrollableContainer):
    def __init__(self, *args, **kwargs):
        ScrollableContainer.__init__(self, *args, **kwargs)
        self.labels = []

    def add(self, text):
        new_label = Label(self.content, text=text)
        new_label.grid(row=len(self.labels),
                       sticky=N+W)
        self.labels.append(new_label)
        self.reset_scrollregion()
        self.scrollable.yview(MOVETO, 1)

    def try_callback(self, callback,
                     failure_message="Error: {0.message}",
                     *args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except Exception as e:
            self.add(failure_message.format(e))
            return None

if __name__ == '__main__':
    from Tkinter import Tk
    import time
    root = Tk()
    hf = HistoryFrame(root)
    hf.grid()
    hf.add("Hellooooooo sexy!")
    for i in range(20):
        root.after(500*(1+i), hf.add, str(i))
    root.mainloop()
