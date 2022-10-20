import tkinter as tk
from handler import Handler, HandlerModes


class MainWindow:
    window = tk.Tk()
    textbox = tk.Text()

    def __init__(self, mode=HandlerModes.Highlight):
        self.window.geometry(f'600x400')
        self.window.title('Spellchecker')

        self.textbox.pack()
        self.textbox.bind("<<Modified>>", self.textbox_callback)
        self.textbox.tag_configure('red', foreground='red')
        self.textbox.tag_configure('default', foreground='black')
        self.textbox.tag_lower('default', 'red')

        self.mode = mode
        self.handler = Handler.create(self.mode)

        self.textbox.focus()
        self.window.mainloop()

    def textbox_callback(self, virtual):
        text = self.textbox.get('1.0', tk.END)
        tokens, needs_edit = self.handler.handle(text)

        if self.mode == HandlerModes.Highlight:
            self.textbox.tag_remove('red', '1.0', tk.END)
            for word, indexes in tokens.items():
                self.textbox.tag_add('red', indexes[0], indexes[1])

        if self.mode == HandlerModes.Autocorrect and needs_edit:
            value = list(tokens.items())[0]
            word = value[0]
            indexes = value[1]

            self.textbox.replace(indexes[0], indexes[1], word)

        self.textbox.edit_modified(False)


