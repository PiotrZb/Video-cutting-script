# Video-cutting-script
A script to download YouTube videos and cut frames from them

## Directory tree

<div>
    <span >└── Project/</span>
    <div style="margin-left: 30px"> 
        <span >├── src/</span>
        <div style="margin-left: 30px"> 
            <span >├── main.py</span><br>
            <span >├── gui.py</span><br>
            <span >├── settings.py</span><br>
            <span >├── pathmanager.py</span><br>
            <span >├── Pages/</span>
            <div style="margin-left: 30px"> 
                <span >├── CutWindow.py</span><br>
                <span >├── DownloadWindow.py</span><br>
                <span >├── FrameLabelingWindow.py</span><br>
                <span >├── Menu.py</span><br>
            </div>
        </div>
        <span >├── Data/</span>
        <div style="margin-left: 30px"> 
            <span >├── Downloads/</span><br>
            <span >├── Frames/</span><br>
            <span >├── Labels/</span><br>
            <span >├── Res/</span><br>
            <span >├── Videos/</span>
        </div>
    </div>
</div>

## Installation

### MacOS (ARM silicon)

You will need to install Rosetta2 emulator for the new ARM silicon 

```
$ /usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

After installing Rosetta2 above you can then use the Homebrew cmd and install Homebrew for ARM M1 chip: 

```
$ arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Install Tkinter using Homebrew

```
$ arch -x86_64 brew install python-tk
```

### MacOS (Intel)

Install Homebrew

``` 
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

You will need to install Tkinter using Homebrew

```
$ brew install python-tk
```


## Usage

Paste the links to the url_list.txt file in the "Res" folder. <br />
Each link should be on a separate line in the text file. <br />
The videos will be saved in the "Downloads" folder.
