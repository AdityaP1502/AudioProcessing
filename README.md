# Audio Processing Python

An Implementation on various Audio Effects such as reverb, delay, and more. 

## Installation
To install, make sure you have python >= 3.8, python 3.10 is recommended. Then, run this command to install all the libraries used. 

First, clone this repository
```sh
git clone []
```

Then, create a virtual environment in python. 

```sh
py -m venv env
```

After that, activate the virtual environment. 
```sh
./env/Scripts/activate
```

Finally, install the dependencies:
```sh
py -m pip i -r requirements.txt
```

## Run
To run the program, firstly, you need to create a wav file called temp.wav. If your audio file is in .mp3 format, first copy that audio file into ./music folder. Then, run this command:

```sh
python music/convert_mp3_to_wav.py [music_name]
```

If you have the audio file temp/temp.wav, then run this command to apply reverb effects for your audio file:

```sh
python test_components.py
```

Your result audio file is located in temp folder called result.wav
