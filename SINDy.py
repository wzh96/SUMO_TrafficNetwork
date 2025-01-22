import numpy as np
import pandas as pd
import pysindy as psd
from utilis import sindy_params


def SINDy_Train(x, dx, u, threshold = 0.002, polydegree = 2):
    # Train a SINDy model
    library = psd.ConcatLibrary(
        [psd.PolynomialLibrary(degree=polydegree, include_bias=True)])
    model = psd.SINDy(optimizer=psd.STLSQ(threshold=threshold), feature_library=library)
    model.fit(x, u=u, t=1, x_dot=dx)
    return model

def SINDy_Dynamics(x, dx, u, threshold = 0.002):
    # # remove the first 5 seconds
    # x = x.iloc[2:, :].reset_index(drop=True)
    # dx = dx.iloc[2:, :].reset_index(drop=True)
    # u = u.iloc[2:, :].reset_index(drop=True)

    # call SINDy to obtain the dynamics model (ODE)
    model = SINDy_Train(x=x, dx=dx, u=u, threshold=threshold)

    equations = model.equations(precision=6)

    # change the equations format to casadi readable format
    for i in range(len(equations)):
        equations[i] = equations[i].replace(' ', ' * ')
        equations[i] = equations[i].replace('* + *', '+')
        equations[i] = equations[i].replace('^2', '**2')
        equations[i] = equations[i].replace('^3', '**3')

    return equations

def DMD_Train(x, u, threshold = 0):
    # Train a SINDy model
    library = psd.ConcatLibrary(
        [psd.PolynomialLibrary(degree=1, include_bias=False)])
    model = psd.SINDy(optimizer=psd.STLSQ(threshold=threshold), feature_library=library, discrete_time=True)
    model.fit(x=x, u=u, t=1)
    return model

def DMD_Dynamics(x, u, threshold = 0):
    # # remove the first 5 seconds
    # x = x.iloc[2:, :].reset_index(drop=True)
    # dx = dx.iloc[2:, :].reset_index(drop=True)
    # u = u.iloc[2:, :].reset_index(drop=True)

    # call SINDy to obtain the dynamics model (ODE)
    model = DMD_Train(x=x, u=u, threshold=threshold)

    equations = model.equations(precision=6)

    # change the equations format to casadi readable format
    for i in range(len(equations)):
        equations[i] = equations[i].replace('[k]', "")
        equations[i] = equations[i].replace(' ', ' * ')
        equations[i] = equations[i].replace('* + *', '+')

    return equations

'0.938560 x0[k] + -0.075411 x1[k] + -0.039870 x2[k] + -2.778009 x3[k] + 0.018813 x4[k] + 0.117007 x5[k] + 0.088310 x6[k] + 0.109364 x7[k] + 0.193331 u0[k] + -0.013690 u1[k] + -0.018547 u2[k] + -0.002732 u3[k] + -0.005210 u4[k] + -0.643598 u5[k]'