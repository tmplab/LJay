
apt install git python-pip libasound2-dev python-dev 
git clone https://github.com/ptone/pyosc
cd pyosc/
python setup.py install
git clone https://github.com/pyserial/pyserial/
cd pyserial/
python setup.py install

pip install pysimpledmx
pip install Cython
pip install mido
pip install rtmidi python-rtmidi tokenize
pip install pygame

