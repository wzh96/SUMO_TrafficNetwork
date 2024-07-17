import numpy as np
import pandas as pd
import pysindy as psd


def SINDy_Train(x, dx, u):
    # Train a SINDy model
    library = psd.ConcatLibrary(
        [psd.PolynomialLibrary(degree=2)])
    model = psd.SINDy(optimizer=psd.STLSQ(threshold=1e-4), feature_library=library)
    model.fit(x, u=u, t=1, x_dot=dx)

    Theta = np.array(library.transform(pd.concat([x, u], axis=1)))
    SINDy_coeff = np.transpose(model.coefficients())
    equations = model.equations(precision=6)

    return Theta, SINDy_coeff, equations

def SINDy_Dynamics(x, dx, u):
    # remove the first 5 seconds
    x = x.iloc[5:, :].reset_index(drop=True)
    dx = dx.iloc[5:, :].reset_index(drop=True)
    u = u.iloc[5:, :].reset_index(drop=True)

    # call SINDy to obtain the dynamics model (ODE)
    Theta, SINDy_Coeff, equations = SINDy_Train(x=x, dx=dx, u=u)

    # change the equations format to casadi readable format
    for i in range(len(equations)):
        equations[i] = equations[i].replace(' ', ' * ')
        equations[i] = equations[i].replace('* + *', '+')
        equations[i] = equations[i].replace('^', '**')

    return equations