# Hamtech_Rasa
## virtual env
    1- make virtual env with "python -m venv venv"
    2- with "source venv/bin/activate" activate virtual env
## pakage installing
    3- Use requirment.txt for pip install (pip install -r requirment.txt)
## stanza loader
    !- go to this page, for setup stanza!(https://github.com/RasaHQ/rasa-nlu-examples) (if stanza isn't corectly installed!)
        Use "pip install "rasa_nlu_examples[stanza] @ git+https://github.com/RasaHQ/rasa-nlu-examples.git"" command to install the package

    4- run stanza_loader.py to download pretrained model
## rasa_train
    5- after all with "rasa train" command, in terminal, make a training model!
## Run
Done! with "rasa shell" you can use chatbot :)