def prepareNumpy():
    import os

    os.environ["OMP_NUM_THREADS"] = '8'  # export OMP_NUM_THREADS=4
    os.environ["OPENBLAS_NUM_THREADS"] = '8'  # export OPENBLAS_NUM_THREADS=4
    os.environ["MKL_NUM_THREADS"] = '8'  # export MKL_NUM_THREADS=6
