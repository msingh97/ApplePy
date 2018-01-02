from os import popen
from subprocess import Popen, PIPE

def beep():
    """Makes the Mac's iconic beep noise to indicate an error."""
    popen("osascript -e 'beep'")


def get_clipboard():
    """Returns the contents current user clipboard as a string."""
    return popen("osascript -e 'the clipboard'").read().strip()


#TODO: FIX SET CLIPBOARD AND OPEN URL POPEN METHODS

def set_clipboard(s):
    """Sets the user's clipboard to string s."""
    assert isinstance(s, str), "Clipboard must be set to a string."
    popen("osascript -e 'set the clipboard to \"{0}\"'".format(s))


def open_url(url):
    popen("osascript -e 'open location \"{0}\"'".format(url))
