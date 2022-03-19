1. Open a new terminal and cd into major_project/pocket-sphinx-language-model/

1. Ensure the dependicies are installed using the commands:
    * sudo apt-get install -y python python-dev python-pip build-essential swig libpulse-dev git
    * sudo apt-get install python-pyaudio
    
1. Next install pocketsphinx for Python using the following command:
    * sudo pip install pocketsphinx
    
1. Now use the following commands to create the directories required for pocketsphinx:
    * sudo mkdir /usr/share/pocketsphinx
    * sudo mkdir /usr/share/pocketsphinx/model
    * sudo mkdir /usr/share/pocketsphinx/model/hmm
    * sudo mkdir /usr/share/pocketsphinx/model/hmm/en_US

1. Finally use the following command to copy the language model
    * sudo cp -r hub4wsj_sc_8k/ /usr/share/pocketsphinx/model/hmm/en_US/

pocketsphinx should be ready for use now.
