import numpy as np
import pandas as pd
import pysindy as psd
from utilis import sindy_params


def SINDy_Train(x, dx, u, threshold = 0.002):
    # Train a SINDy model
    library = psd.ConcatLibrary(
        [psd.PolynomialLibrary(degree=2, include_bias=True)])
    model = psd.SINDy(optimizer=psd.STLSQ(threshold=threshold), feature_library=library)
    model.fit(x, u=u, t=1, x_dot=dx)
    return model

def SINDy_Dynamics(x, dx, u, threshold = 0.002):
    # remove the first 5 seconds
    x = x.iloc[5:, :].reset_index(drop=True)
    dx = dx.iloc[5:, :].reset_index(drop=True)
    u = u.iloc[5:, :].reset_index(drop=True)

    # call SINDy to obtain the dynamics model (ODE)
    model = SINDy_Train(x=x, dx=dx, u=u, threshold=threshold)

    equations = model.equations(precision=6)

    # change the equations format to casadi readable format
    for i in range(len(equations)):
        equations[i] = equations[i].replace(' ', ' * ')
        equations[i] = equations[i].replace('* + *', '+')
        equations[i] = equations[i].replace('^2', '**2')

    return equations