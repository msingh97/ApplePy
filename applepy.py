import os


def dialog(s, buttons=[], default_button=""):
    """Displays a dialog, and returns the text in the button that the user clicked."""
    assert not buttons or isinstance(buttons, list), "Buttons must be specified in list format."
    assert not default_button or default_button in buttons, "Default button must be one of the listed buttons."
    if default_button:
        default_button = "default button \"" + default_button + "\""
    if buttons:
        for i in buttons:
            assert isinstance(i, str), "Button names must be in string format."
            button_str = "{" + ", ".join(['"{0}"'.format(i) for i in buttons]) + "}"
        query = "osascript -e 'button returned of (display dialog \"{0}\" buttons {1} {2})'".format(s, button_str,
                                                                                                    default_button)
    else:
        query = "osascript -e 'button returned of (display dialog \"{0}\" {1})'".format(s, default_button)
    return os.popen(query).read().strip()


def input_box(message, placeholder='', submit_button="Submit"):
    """Input box with two buttons: 'Cancel' and the submit_button parameter (default 'Submit'). Returns the inputted
    text if the user clicks the submit button."""
    assert isinstance(message, str), "Message must be a string."
    assert isinstance(submit_button, str), "submit_button parameter must be of type string."
    submit_button = "buttons {\"Cancel\", \"" + submit_button + "\"} default button \"" + submit_button + "\""
    query = "osascript -e 'text returned of (display dialog \"{0}\" {1} default answer \"{2}\")'".format(message,
                                                                                                         submit_button,
                                                                                                         placeholder)
    return os.popen(query).read().strip()


def select_from_list(*options):
	"""Prompts the user to make a selection from a list with options specified as arguments."""
	assert len(options) > 0, "Must specify at least one list option."
	option_str = "{\"" + "\" , \"".join(options) + "\"}"
	return os.popen("osascript -e 'choose from list {0}'".format(option_str)).read().strip()


def file_selector():
	"""Prompts the user to select a file from the device, and returns the file's path."""
	path = os.popen("osascript -e 'choose file'").read().strip().split(":")
	return ("/").join(path)[6:]


def folder_selector():
	"""Prompts the user to select a folder from the device, and returns the folder's path."""
	path = os.popen("osascript -e 'choose folder'").read().strip().split(":")
	return ("/").join(path)[6:]


def application_selector():
	"""Prompts the user to select an application installed on the device, and returns the name of the applicaiton."""
	return os.popen("osascript -e 'choose application'").read().strip()


_speech_voices = ["Alex", "Agnes", "Allison", "Ava", "Kathy", "Princess", "Samantha", "Susan", "Vicki", "Victoria,"
                  "Bruce", "Fred", "Junior", "Ralph", "Tom", "Albert", "Bad News", "Bahh", "Bells", "Cellos",
                  "Deranged", "Good News", "Hysterical", "Pipe Organ", "Trinoids", "Whisper", "Zarvox"]


def speak(s, voice="Alex"):
    # TODO: finish docstring
    """Uses the Mac's speech-to-text features to say the inputted string. The default voice is 'Alex', which 
    is available on Mac OSX 10.6 and higher for English (US) configured Macs. The user may input another voice by 
    specifying a valid voice name in the voice parameter (ie. 'Cellos'). A list of all valid voices is available on the 
    Mac System Preferences/Speech and Dialog menu; all English (US) voices are in the list returned from 
    show_speech_voices()."""
    assert isinstance(s, str), "Speech input must be a string."
    os.popen("osascript -e 'say \"{0}\" using \"{1}\"'".format(s, voice))


def show_speech_voices():
    """Returns a list of valid voices that may be used with the speak() function. Currently, only English (US) voices
     are listed."""
    return _speech_voices[:]


def beep():
    """Makes the Mac's iconic beep."""
    os.popen("osascript -e 'beep'")


def get_clipboard():
    """Returns the current user clipboard."""
    return os.popen("osascript -e 'the clipboard'").read().strip()


def set_clipboard(s):
    """Sets the user's clipboard to string s."""
    assert isinstance(s, str), "Clipboard must be set to a string."
    os.popen("osascript -e 'set the clipboard to \"{0}\"'".format(s))


def open_url(url):
	os.popen("osascript -e 'open location \"{0}\"'".format(url))



