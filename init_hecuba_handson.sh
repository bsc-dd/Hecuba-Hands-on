#!/bin/bash

cd /opt

# Activate virtualenv for hecuba
source /opt/venv-hecuba/bin/activate

# Install Hecuba
pip3 install hecuba --upgrade

# Clone hands-on
git clone https://github.com/polsm91/Hecuba-Hands-on.git /opt/hecuba_handson

cd /opt/hecuba_handson

# Launch Jupyter notebook
jupyter notebook --ip=0.0.0.0 --NotebookApp.token=''
