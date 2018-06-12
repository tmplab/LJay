

# Install debian deps
sudo apt install libpython-dev libjack-dev
# Install python specific deps
sudo pip install mido rtmidi scipy pygame pysimpledmx pyserial
sudo pip install --pre python-rtmidi
git clone https://github.com/ptone/pyosc --depth 1 /tmp/pyosc && cd /tmp/pyosc && sudo ./setup.py install 
 
