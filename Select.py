from subprocess import Popen, PIPE


class Selection:
    """Prompts the user to make a selection when prompted. Users can select a string from a list, an application on the
    device, or a file on the device. If the user must select from a list, the user's selection is returned as a string.
    An App object is returned if the user selects an application, and a File object is returned if the user selects a 
    file."""
    def __init__(self):
        self.__method, self.__param = None, None

    def list(self, *args):
        self.__method = "list"
        self.__param = [i if isinstance(i, str) else str(i) for i in args]
        return self

    def application(self):
        self.__method = "application"
        return self

    def file(self):
        self.__method = "file"
        return self

    def run(self):
        assert self.__method, "A method must be specified before execution."
        if self.__method == "list":
            args = ["osascript", "./scpt/select.scpt", "list"] + self.__param
        else:
            args = ["osascript", "./scpt/select.scpt", "choose", self.__method]
        output = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                                  shell=False)
        if self.__method == "list":
            return output.stdout.readline().decode('utf-8').strip()
        elif self.__method == "application":
            return App(output.stdout.readline().decode('utf-8').strip())
        elif self.__method == "file":
            filename = output.stdout.readline().decode('utf-8').strip()
            path = output.stdout.readline().decode('utf-8').strip()
            extension = output.stdout.readline().decode('utf-8').strip()
            date_created = output.stdout.readline().decode('utf-8').strip()
            last_modified = output.stdout.readline().decode('utf-8').strip()
            return File(filename, path, extension, date_created, last_modified)
        return output


class File:
    """Holds key information about a file on the user device, and contains a method to open the file 
    with the default application."""
    def __init__(self, name, mac_path, file_extension, date_created, last_modified):
        self.__filename = name
        self.__path = mac_path
        self.__unix_path = __clean_path(mac_path)
        self.extension = file_extension
        self.date_created = date_created
        self.last_modified = last_modified

    def open(self):
        Popen(["osascript", "./scpt/open.scpt", "file", self.__path], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

    def __str__(self):
        return self.__filename

    def __repr__(self):
        return self.__unix_path


class App:
    """Holds the name of an application [use str() or repr()], and a method to open the application with the default 
    program if one exists."""
    def __init__(self, app_name):
        self.__name = app_name

    def open(self):
        Popen(["osascript", "./scpt/open.scpt", "application", self.__name], stdin=PIPE, stdout=PIPE, stderr=PIPE,
              shell=False)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name


def __clean_path(path):
    """Converts a file path from Mac style to Unix style."""
    path = path.split(":")
    for i in range(len(path)):
        s = path[i]
        if " " in s or "/" in s:
            path[i] = '"{}"'.format(s)
    return "/".join(path)