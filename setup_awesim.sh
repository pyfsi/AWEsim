#!/bin/bash

# Assumes AWEsim to be installed in ~/Software
# Will place other software dependencies also in ~/Software

# =============================================================================
## Install CoCoNuT branch AWEsim
# =============================================================================

cd ~/Software || exit 1
export SOFTWAREPATH=$PWD

if [ ! -d "coconut" ]; then
    git clone --single-branch --branch AWEsim https://github.com/pyfsi/coconut coconut
else
    echo "coconut already exists, skipping clone."
fi

# =============================================================================
## Install AWEbox and requirements 
# =============================================================================

# TODO: put AWEsim_largefiles on FM (non-personal) account
# TODO: Install from awebox GitHub? (first test compatibility)


if [ ! -d "awebox" ]; then

    module load Anaconda3-python/2024.02-1
    module load ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5

    mkdir tools
    export PIP_TARGET=$SOFTWAREPATH/tools 
    pip install -r AWEsim/requirements.txt
    
    scp /cfdfile1/data/fm/niels/AWEsim_largefiles/awebox/awebox.zip $SOFTWAREPATH
    scp /cfdfile1/data/fm/niels/AWEsim_largefiles/awebox/hsl.zip $SOFTWAREPATH

    unzip awebox.zip
    unzip hsl.zip

    cd hsl
    tar -xvzf coinhsl-2021.05.05.tar.gz
    tar -xvzf metis-4.0.3.tar.gz
    mv ./metis-4.0.3 ./coinhsl-2021.05.05/.

    sed -i 's/METIS\_NODEND/metis\_nodend\_/' coinhsl-2021.05.05/loadmetis/loadmetis.c
    sed -i 's/\$HOME\/Tools\/hsl/\$SOFTWAREPATH\/hsl/' compile_libcoinhsl.sh

    cp compile_libcoinhsl.sh coinhsl-2021.05.05/.
    chmod +x coinhsl-2021.05.05/compile_libcoinhsl.sh

    cd coinhsl-2021.05.05
    ./compile_libcoinhsl.sh

    cd ../..
    ln -s $SOFTWAREPATH/hsl/coinhsl-2021.05.05/lib/libcoinhsl.so $SOFTWAREPATH/tools/casadi/libhsl.so

    cd ~/Software
    mv hsl ./tools/
    rm awebox.zip
    rm hsl.zip

else
    echo "awebox already exists, skipping installation."
fi


# =============================================================================
## Install mshGen (TODO)
# =============================================================================


# =============================================================================
## Configure .bashrc (To be completed)
# =============================================================================

MARKER="# --- AWEsim environment settings ---"

if ! grep -Fq "$MARKER" ~/.bashrc; then
    cat >> ~/.bashrc << 'EOF'

# --- AWEsim environment settings ---
module load Anaconda3-python/2024.02-1
export PYTHONPATH=${HOME}/Software:$PYTHONPATH

set_awebox(){

# Required modules...
module load Anaconda3-python/2024.02-1
module load ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5

# HPC
# module load ScaLAPACK/2.2.0-gompi-2023a-fb

# Required path variables
export PYTHONPATH=$PYTHONPATH:$HOME/Software/awebox
export PYTHONPATH=$PYTHONPATH:$HOME/Software/tools
export PYTHONPATH=$PYTHONPATH:$HOME/Software/tools/casadi
export CASADIPATH=$HOME/Software/tools/casadi
export CASADIPATH=$HOME/Software/tools/casadi/casadi
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CASADIPATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Software/tools/hsl/coinhsl-2021.05.05/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/Software/tools/hsl/coinhsl-2021.05.05/metis-4.0.3/Lib
}

# --- End AWEsim environment settings ---

EOF

    echo "AWEsim environment settings added to ~/.bashrc"
else
    echo "AWEsim environment settings already exist in ~/.bashrc"
fi

# =============================================================================
## Download example (CFD) files from UGent FM cluster and prepare examples
# =============================================================================

# TODO: put AWEsim_largefiles on FM (non-personal) account
# TODO: check if files already exist before copying

cd ~/Software

mkdir ./AWEsim/cases/case_megawes_maneuvres/SIM0_rolling_CSD/CFD/
mkdir ./AWEsim/cases/case_megawes_maneuvres/SIM0_rolling_CSD/CFD/Results
mkdir ./AWEsim/cases/case_megawes_maneuvres/SIM0_rolling_CSD/CFD/Results_debug

scp /cfdfile1/data/fm/niels/AWEsim_largefiles/cases/case_megawes_maneuvres/simulation* ./AWEsim/cases/case_megawes_maneuvres/SIM0_rolling_CSD/CFD/



