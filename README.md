# Video-cutting-script
A script to download YouTube videos and cut frames from them

## Installation

### MacOS (ARM silicon)

You will need to install Rosetta2 emulator for the new ARM silicon 

```
$ /usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

After installing Rosetta2 above you can then use the Homebrew cmd and install Homebrew for ARM M1 chip: 

```
$ arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.
com/Homebrew/install/master/install.sh)"
```

Install Tkinter using Homebrew

```
$ arch -x86_64 brew install python-tk
```

### MacOS (Intel)

Install Homebrew

``` 
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.
com/Homebrew/install/HEAD/install.sh)"

```

You will need to install Tkinter using Homebrew

```
$ brew install python-tk
```


## Usage

Paste the links to the url_list.txt file in the "Res" folder. <br />
Each link should be on a separate line in the text file. <br />
The videos will be saved in the "Downloads" folder.
