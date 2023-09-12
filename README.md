# **🛠️ Video-cutting-script 🛠️**

An integrated tool that allows you to create databases for training the YOLO algorithm.<br />
Features:
* videos downloading
* frames extraction
* frames labeling

## Directory tree 🗃️
```bash
.
└── Video-cutting-script/
    ├── Data/
    │   ├── Downloads/
    │   ├── Frames/
    │   ├── Labels/
    │   ├── Res/
    │   └── Videos/
    ├── src/
    │   ├── ConsoleGui/
    │   │   ├── cmenu.py
    │   │   └── functions.py
    │   ├── Pages/
    │   │   ├── __init__.py
    │   │   ├── CutWindow.py
    │   │   ├── DownloadWindow.py
    │   │   ├── FrameLabellingWindow.py
    │   │   └── Menu.py
    │   ├── __init__.py
    │   ├── gui.py
    │   ├── pathmanger.py
    │   └── settings.py
    ├── main.py
    ├── setup.py
    ├── README.md
    └── requirements.txt
```

## Installation ⚙️

### MacOS (ARM silicon)

You will need to install Rosetta2 emulator for the new ARM silicon 

```bash
$ /usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

After installing Rosetta2 above you can then use the Homebrew cmd and install Homebrew for ARM M1 chip: 

```bash
$ arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Install Tkinter using Homebrew

```bash
$ arch -x86_64 brew install python-tk
```

### MacOS (Intel)

Install Homebrew

```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

You will need to install Tkinter using Homebrew

```bash
$ brew install python-tk
```


## Usage 👈

Paste the links to the url_list.txt file in the "Res" folder. <br />
Each link should be on a separate line in the text file. <br />
The videos will be saved in the "Downloads" folder.<br />

Use video cutter module to extract frames from downloaded videos. <br />
Thanks to the preview, you will be able to easly select interesting fragment. <br />
If you want, you can add a prefix to the title of the extracted frames.<br />

Labeling module allows you to create YOLO labels for exracted frames. <br />
To make thinks easyer we added following keybindings:<br />
* previous frame <kbd>A</kbd>
* next frame <kbd>D</kbd>
* save labels <kbd>S</kbd>
* clear bboxes <kbd>C</kbd>

## GUI 🎨

* ### Menu 📜
  
<br>
<p align="center">
    <img width="202" alt="image" src="https://github.com/PiotrZb/Video-cutting-script/assets/84187115/151b94ad-3a7d-46cd-9eb5-dc1b5debfcbb"><br />
</p>
<br>

* ### Video downloading module ⬇️

<br>
<p align="center">
    <img width="352" alt="image" src="https://github.com/PiotrZb/Video-cutting-script/assets/84187115/5b3c16a9-4cab-43ac-8180-8c91fcc8e3f0"><br />
</p>
<br>

* ### Video cutting module ✂️

<br>
<p align="center">
    <img width="352" alt="image" src="https://github.com/PiotrZb/Video-cutting-script/assets/84187115/c759a17f-0bb3-4148-a44a-3399a4992e7a"><br />
</p>
<br>

* ### Frames labeling module 🏷️

<br>
<p align="center">
    <img width="267" alt="image" src="https://github.com/PiotrZb/Video-cutting-script/assets/84187115/d86fb3aa-e9e1-4d07-86ba-cc3722d51a07"><br />
</p>
<br>

## License :page_facing_up:
[License](LICENSE)
