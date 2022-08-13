# Py-Reader


A simple *Text-To-Speech* application written in Python using [Pyttsx3](https://pyttsx3.readthedocs.io/en/latest/.html) [^1] and [Tkinter](https://docs.python.org/3/library/tkinter.html). Py-Reader acts a as GUI wrapper over basic pyttsx3 commands with the ability to read along with subtitles and adjust settings as needed.

![main_menu](https://user-images.githubusercontent.com/10747624/184461506-17847654-860a-4cf9-8a20-cb117e86a456.png)

### Features
* Select and read Text (_.txt_) files
* Read along with subtitles
* Start, stop and resume reading as needed [^2]
* Control the Rate of Speech (soft locked at 75 ~ 225)
* ~~Control the volume~~ [^3]
* Change voice (*if available*)


###### Built using
| Software | Version  |
| -------- | --------:|
| Python3  | 3.8.10 |
| pyttsx3  | 2.6 |
| tkinter  | 2.90 |



### Dependencies
> via pip
~~~~
pip install pyttsx3
~~~~

> via apt-get
~~~~
xargs -a packages.txt sudo apt-get install
~~~~

The application can be started in the root directory using:
~~~~
python3 scripts/py-reader.py
~~~~

### Credits

> Main background: [KeronnArt](https://iconscout.com/illustration/book-reading-5514316)

> Settings background: [Leovinus](https://pixabay.com/vectors/info-icon-information-message-tips-803717/)

> Info icon: [Torres Store](https://www.kindpng.com/imgv/Jhimim_gear-clipart-gear-box-blue-setting-icon-png/)



---
[^1]: pyttsx3 uses different synthesizers based on the envirenment so additional dependencies may be required [link](https://pyttsx3.readthedocs.io/en/latest/support.html)

[^2]: At this time the TTS function cannot be interupped mid-sentence and will finsh the current line before stopping. This may cause an unintended bug of audio overlapping if commands are issued too quickly.

[^3]: Setting the volume property dymanically has caused audio issues during testing. The line in question has been left in as a comment in case others wish to modify the the project in the future.
