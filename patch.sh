#!/bin/bash
cd /opt

# Activate virtualenv for hecuba
source /opt/venv-hecuba/bin/activate

sudo /opt/venv-hecuba/bin/pip install --upgrade hecuba
