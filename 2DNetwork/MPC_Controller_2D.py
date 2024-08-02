import do_mpc
from casadi import *

def Flow_Dynamics_Model(equations):
    # define model type as continuous
    model_type = 'continuous'
    model = do_mpc.model.Model(model_type)

    x0 = model.set_variable(var_type='_x', var_name='x0', shape=(1, 1))
    x1 = model.set_variable(var_type='_x', var_name='x1', shape=(1, 1))
    x2 = model.set_variable(var_type='_x', var_name='x2', shape=(1, 1))
    x3 = model.set_variable(var_type='_x', var_name='x3', shape=(1, 1))
    x4 = model.set_variable(var_type='_x', var_name='x4', shape=(1, 1))
    x5 = model.set_variable(var_type='_x', var_name='x5', shape=(1, 1))
    x6 = model.set_variable(var_type='_x', var_name='x6', shape=(1, 1))
    x7 = model.set_variable(var_type='_x', var_name='x7', shape=(1, 1))

    u0 = model.set_variable(var_type='_u', var_name='u0', shape=(1, 1))
    u1 = model.set_variable(var_type='_u', var_name='u1', shape=(1, 1))
    u2 = model.set_variable(var_type='_u', var_name='u2', shape=(1, 1))
    u3 = model.set_variable(var_type='_u', var_name='u3', shape=(1, 1))
    u4 = model.set_variable(var_type='_u', var_name='u4', shape=(1, 1))
    u5 = model.set_variable(var_type='_u', var_name='u5', shape=(1, 1))
    # u6 = model.set_variable(var_type='_u', var_name='u6', shape=(1, 1))
    # u7 = model.set_variable(var_type='_u', var_name='u7', shape=(1, 1))

    model.set_rhs('x0', eval(equations[0]))
    model.set_rhs('x1', eval(equations[1]))
    model.set_rhs('x2', eval(equations[2]))
    model.set_rhs('x3', eval(equations[3]))
    model.set_rhs('x4', eval(equations[4]))
    model.set_rhs('x5', eval(equations[5]))
    model.set_rhs('x6', eval(equations[6]))
    model.set_rhs('x7', eval(equations[7]))

    model.setup()

    return model


def MPC_Controller(model, params, setup_mpc, silence_solver = False):

    param_mterm = params['param_mterm']
    param_lterm = params['param_lterm']
    param_R = params['param_R']
    param_U_upper  = params['param_U_upper']
    param_U_lower = params['param_U_lower']
    param_X_upper = params['param_X_upper']
    param_X_lower = params['param_X_lower']

    mpc = do_mpc.controller.MPC(model)
    mpc.set_param(**setup_mpc)

    mpc.settings.set_linear_solver('mumps')
    if silence_solver:
        mpc.settings.supress_ipopt_output()

    # set model objective function
    # mterm = param_mterm * (-model._x['x0'] - model._x['x1'] - model._x['x2'] - model._x['x3']
    #          - model._x['x4'] - model._x['x5'] - model._x['x6'] - model._x['x7'])
    # lterm = param_lterm * (-model._x['x0'] - model._x['x1'] - model._x['x2'] - model._x['x3']
    #          - model._x['x4'] - model._x['x5'] - model._x['x6'] - model._x['x7'])

    mterm = param_mterm * ((model._x['x0'] - params['desire_occu'])**2 + (model._x['x1'] - params['desire_occu'])**2 +
                            (model._x['x2'] - params['desire_occu'])**2 + (model._x['x3'] - params['desire_occu'])**2 +
                            (model._x['x4'] - params['desire_occu'])**2 + (model._x['x5'] - params['desire_occu'])**2 +
                            (model._x['x6'] - params['desire_occu'])**2 + (model._x['x7'] - params['desire_occu'])**2)

    lterm = param_lterm * ((model._x['x0'] - params['desire_occu'])**2 + (model._x['x1'] - params['desire_occu'])**2 +
                            (model._x['x2'] - params['desire_occu'])**2 + (model._x['x3'] - params['desire_occu'])**2 +
                            (model._x['x4'] - params['desire_occu'])**2 + (model._x['x5'] - params['desire_occu'])**2 +
                            (model._x['x6'] - params['desire_occu'])**2 + (model._x['x7'] - params['desire_occu'])**2)

    # mterm = param_mterm * ((model._x['x0'])**2 + (model._x['x1'])**2 +
    #                         (model._x['x2'])**2 + (model._x['x3'])**2 +
    #                         (model._x['x4'])**2 + (model._x['x5'])**2 +
    #                         (model._x['x6'])**2 + (model._x['x7'])**2)
    #
    # lterm = param_lterm * ((model._x['x0'])**2 + (model._x['x1'])**2 +
    #                         (model._x['x2'])**2 + (model._x['x3'])**2 +
    #                         (model._x['x4'])**2 + (model._x['x5'])**2 +
    #                         (model._x['x6'])**2 + (model._x['x7'])**2)


    mpc.set_objective(mterm=mterm, lterm=lterm)

    mpc.set_rterm(
        u0=param_R,
        u1=param_R,
        u2=param_R,
        u3=param_R,
        u4=param_R,
        u5=param_R
        # u6=param_R,
        # u7=param_R
    )

    # state lower bound
    mpc.bounds['lower', '_x', 'x0'] = param_X_lower
    mpc.bounds['lower', '_x', 'x1'] = param_X_lower
    mpc.bounds['lower', '_x', 'x2'] = param_X_lower
    mpc.bounds['lower', '_x', 'x3'] = param_X_lower
    mpc.bounds['lower', '_x', 'x4'] = param_X_lower
    mpc.bounds['lower', '_x', 'x5'] = param_X_lower
    mpc.bounds['lower', '_x', 'x6'] = param_X_lower
    mpc.bounds['lower', '_x', 'x7'] = param_X_lower

    # state upper bound
    mpc.bounds['upper', '_x', 'x0'] = param_X_upper
    mpc.bounds['upper', '_x', 'x1'] = param_X_upper
    mpc.bounds['upper', '_x', 'x2'] = param_X_upper
    mpc.bounds['upper', '_x', 'x3'] = param_X_upper
    mpc.bounds['upper', '_x', 'x4'] = param_X_upper
    mpc.bounds['upper', '_x', 'x5'] = param_X_upper
    mpc.bounds['upper', '_x', 'x6'] = param_X_upper
    mpc.bounds['upper', '_x', 'x7'] = param_X_upper

    # control lower bound
    mpc.bounds['lower', '_u', 'u0'] = param_U_lower
    mpc.bounds['lower', '_u', 'u1'] = param_U_lower
    mpc.bounds['lower', '_u', 'u2'] = param_U_lower
    mpc.bounds['lower', '_u', 'u3'] = param_U_lower
    mpc.bounds['lower', '_u', 'u4'] = param_U_lower
    mpc.bounds['lower', '_u', 'u5'] = param_U_lower
    # mpc.bounds['lower', '_u', 'u6'] = param_U_lower
    # mpc.bounds['lower', '_u', 'u7'] = param_U_lower

    # control upper bound
    mpc.bounds['upper', '_u', 'u0'] = param_U_upper
    mpc.bounds['upper', '_u', 'u1'] = param_U_upper
    mpc.bounds['upper', '_u', 'u2'] = param_U_upper
    mpc.bounds['upper', '_u', 'u3'] = param_U_upper
    mpc.bounds['upper', '_u', 'u4'] = param_U_upper
    mpc.bounds['upper', '_u', 'u5'] = param_U_upper
    # mpc.bounds['upper', '_u', 'u6'] = param_U_upper
    # mpc.bounds['upper', '_u', 'u7'] = param_U_upper

    # set terminal lower bound for the state
    mpc.terminal_bounds['lower', 'x0'] = param_X_lower
    mpc.terminal_bounds['lower', 'x1'] = param_X_lower
    mpc.terminal_bounds['lower', 'x2'] = param_X_lower
    mpc.terminal_bounds['lower', 'x3'] = param_X_lower
    mpc.terminal_bounds['lower', 'x4'] = param_X_lower
    mpc.terminal_bounds['lower', 'x5'] = param_X_lower
    mpc.terminal_bounds['lower', 'x6'] = param_X_lower
    mpc.terminal_bounds['lower', 'x7'] = param_X_lower


    # set terminal upper bound for the state
    mpc.terminal_bounds['upper', 'x0'] = param_X_upper
    mpc.terminal_bounds['upper', 'x1'] = param_X_upper
    mpc.terminal_bounds['upper', 'x2'] = param_X_upper
    mpc.terminal_bounds['upper', 'x3'] = param_X_upper
    mpc.terminal_bounds['upper', 'x4'] = param_X_upper
    mpc.terminal_bounds['upper', 'x5'] = param_X_upper
    mpc.terminal_bounds['upper', 'x6'] = param_X_upper
    mpc.terminal_bounds['upper', 'x7'] = param_X_upper

    mpc.setup()

    return mpc
