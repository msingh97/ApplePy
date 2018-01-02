from subprocess import Popen, PIPE


class Dialog():
    def __init__(self, message_text):
        self.message = message_text
        self.buttons, self.default_button = None, None
        self.input = None

    def with_buttons(self, *button_names):
        assert len(button_names) >= 1, "Must specify at least one button."
        assert len(button_names) <= 3, "Only up to three buttons may be specified."
        assert self.default_button is None or self.default_button in button_names, "Default button must be one of the specified custom buttons."
        self.buttons = list(button_names)
        return self

    def with_default_button(self, default):
        assert default in self.buttons, "Default button must be one of the specified custom buttons."
        self.default_button = default
        return self

    def with_input(self, input_text=""):
        self.input = input_text
        return self

    def run(self):
        assert self.message, "Message cannot be blank."
        args = ["osascript", "./scpt/dialog.scpt", "display", self.message]
        if self.input is not None:
            args += ["input", self.input]
        if self.buttons:
            if self.default_button:
                args += ["default", self.default_button]
            args.append("buttons")
            args += self.buttons
        output = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
        button = output.stdout.readline().decode('utf-8').strip()
        if self.input is not None:
            text = output.stdout.readline().decode('utf-8').strip()
        else:
            text = None
        return {"button": button, "text": text}
