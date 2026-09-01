#!/bin/bash

# Assumes AWEsim to be installed in ~/Software
# Will place dependencies also in ~/Software

# -
## Install CoCoNuT branch AWEsim
#

cd ~/Software || exit 1

if [ ! -d "coconut" ]; then
    git clone --single-branch --branch AWEsim https://github.com/pyfsi/coconut coconut
else
    echo "coconut already exists, skipping clone."
fi

#
## Install AWEbox (TODO)
#

# Check install.sh script Joris

#
## Install mshGen (TODO)
#

#
## Install python requirements.txt (TODO)
#

#
## Configure .bashrc (To be completed)
#

MARKER="# --- AWEsim environment settings ---"

if ! grep -Fq "$MARKER" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'

# --- AWEsim environment settings ---
module load Anaconda3-python/2024.02-1
export PYTHONPATH=${HOME}/Software:$PYTHONPATH
# --- End AWEsim environment settings ---

EOF

    echo "AWEsim environment settings added to ~/.bashrc"
else
    echo "AWEsim environment settings already exist in ~/.bashrc"
fi

#
## Download example (CFD) files from UGent FM cluster and prepare examples
#
# TODO: put AWEsim_CM_files on FM (non-personal) account
mkdir ./AWEsim/cases/case_megawes_maneuvres/SIM_0_rolling_CSD/CFD/
mkdir ./AWEsim/cases/case_megawes_maneuvres/SIM_0_rolling_CSD/CFD/Results
mkdir ./AWEsim/cases/case_megawes_maneuvres/SIM_0_rolling_CSD/CFD/Results_debug

scp /cfdfile1/data/fm/niels/AWEsim_CM_files/cases/case_megawes_maneuvres/simulation* ./AWEsim/cases/case_megawes_maneuvres/SIM_0_rolling_CSD/CFD/



