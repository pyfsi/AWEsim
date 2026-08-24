set_awesim()
{
# Required modules
module purge
module load Anaconda3-python/2024.02-1

# Required variables mshGen
#ml OpenFOAM/v2112-foss-2021b #These modules interfere with python, dont load
#source $FOAM_BASH
export PYTHONPATH=$PYTHONPATH:$PWD/software
export PYTHONPATH=$PYTHONPATH:$PWD/software/mshGen


# Required variables awebox
# module load ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5
# export PYTHONPATH=$PYTHONPATH:$PWD/awebox
# export PYTHONPATH=$PYTHONPATH:$PWD/tools
# export PYTHONPATH=$PYTHONPATH:$PWD/tools/casadi
# export PYTHONPATH=$PYTHONPATH:$PWD
# export CASADIPATH=$PWD/tools/casadi
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CASADIPATH
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/hsl/coinhsl-2021.05.05/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/hsl/coinhsl-2021.05.05/metis-4.0.3/Lib
}
