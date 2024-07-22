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
    u6 = model.set_variable(var_type='_u', var_name='u6', shape=(1, 1))
    u7 = model.set_variable(var_type='_u', var_name='u7', shape=(1, 1))

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

    coeff_mterm = params['coeff_mterm']
    coeff_lterm = params['coeff_lterm']
    coeff_R = params['coeff_R']

    mpc = do_mpc.controller.MPC(model)
    mpc.set_param(**setup_mpc)

    mpc.settings.set_linear_solver('mumps')
    if silence_solver:
        mpc.settings.supress_ipopt_output()

    # set model objective function
    # mterm = coeff_mterm * (-model._x['x0'] - model._x['x1'] - model._x['x2'] - model._x['x3']
    #          - model._x['x4'] - model._x['x5'] - model._x['x6'] - model._x['x7'])
    # lterm = coeff_lterm * (-model._x['x0'] - model._x['x1'] - model._x['x2'] - model._x['x3']
    #          - model._x['x4'] - model._x['x5'] - model._x['x6'] - model._x['x7'])

    mterm = coeff_mterm * ((fabs(model._x['x0']-params['desire_occu']) + fabs(model._x['x1']-params['desire_occu']) +
                            fabs(model._x['x2']-params['desire_occu'])) + fabs(model._x['x3']-params['desire_occu']) +
                            fabs(model._x['x4']-params['desire_occu']) + fabs(model._x['x5']-params['desire_occu']) +
                            fabs(model._x['x6'] - params['desire_occu']) + fabs(model._x['x7'] - params['desire_occu']))

    lterm = coeff_lterm * ((fabs(model._x['x0'] - params['desire_occu']) + fabs(model._x['x1'] - params['desire_occu']) +
                            fabs(model._x['x2'] - params['desire_occu'])) + fabs(model._x['x3'] - params['desire_occu']) +
                            fabs(model._x['x4'] - params['desire_occu']) + fabs(model._x['x5'] - params['desire_occu']) +
                            fabs(model._x['x6'] - params['desire_occu']) + fabs(model._x['x7'] - params['desire_occu']))


    mpc.set_objective(mterm=mterm, lterm=lterm)

    mpc.set_rterm(
        u0=coeff_R,
        u1=coeff_R,
        u2=coeff_R,
        u3=coeff_R,
        u4=coeff_R,
        u5=coeff_R,
        u6=coeff_R,
        u7=coeff_R
    )

    # state lower bound
    mpc.bounds['lower', '_x', 'x0'] = 1
    mpc.bounds['lower', '_x', 'x1'] = 1
    mpc.bounds['lower', '_x', 'x2'] = 1
    mpc.bounds['lower', '_x', 'x3'] = 1
    mpc.bounds['lower', '_x', 'x4'] = 1
    mpc.bounds['lower', '_x', 'x5'] = 1
    mpc.bounds['lower', '_x', 'x6'] = 1
    mpc.bounds['lower', '_x', 'x7'] = 1

    # state upper bound
    mpc.bounds['upper', '_x', 'x0'] = 80
    mpc.bounds['upper', '_x', 'x1'] = 80
    mpc.bounds['upper', '_x', 'x2'] = 80
    mpc.bounds['upper', '_x', 'x3'] = 80
    mpc.bounds['upper', '_x', 'x4'] = 80
    mpc.bounds['upper', '_x', 'x5'] = 80
    mpc.bounds['upper', '_x', 'x6'] = 80
    mpc.bounds['upper', '_x', 'x7'] = 80

    # control lower bound
    mpc.bounds['lower', '_u', 'u0'] = 20
    mpc.bounds['lower', '_u', 'u1'] = 20
    mpc.bounds['lower', '_u', 'u2'] = 20
    mpc.bounds['lower', '_u', 'u3'] = 20
    mpc.bounds['lower', '_u', 'u4'] = 20
    mpc.bounds['lower', '_u', 'u5'] = 20
    mpc.bounds['lower', '_u', 'u6'] = 20
    mpc.bounds['lower', '_u', 'u7'] = 20

    # control upper bound
    mpc.bounds['upper', '_u', 'u0'] = 180
    mpc.bounds['upper', '_u', 'u1'] = 180
    mpc.bounds['upper', '_u', 'u2'] = 180
    mpc.bounds['upper', '_u', 'u3'] = 180
    mpc.bounds['upper', '_u', 'u4'] = 180
    mpc.bounds['upper', '_u', 'u5'] = 180
    mpc.bounds['upper', '_u', 'u6'] = 180
    mpc.bounds['upper', '_u', 'u7'] = 180

    # set terminal lower bound for the state
    mpc.terminal_bounds['lower', 'x0'] = 1
    mpc.terminal_bounds['lower', 'x1'] = 1
    mpc.terminal_bounds['lower', 'x2'] = 1
    mpc.terminal_bounds['lower', 'x3'] = 1
    mpc.terminal_bounds['lower', 'x4'] = 1
    mpc.terminal_bounds['lower', 'x5'] = 1
    mpc.terminal_bounds['lower', 'x6'] = 1
    mpc.terminal_bounds['lower', 'x7'] = 1


    # set terminal upper bound for the state
    mpc.terminal_bounds['upper', 'x0'] = 80
    mpc.terminal_bounds['upper', 'x1'] = 80
    mpc.terminal_bounds['upper', 'x2'] = 80
    mpc.terminal_bounds['upper', 'x3'] = 80
    mpc.terminal_bounds['upper', 'x4'] = 80
    mpc.terminal_bounds['upper', 'x5'] = 80
    mpc.terminal_bounds['upper', 'x6'] = 80
    mpc.terminal_bounds['upper', 'x7'] = 80

    mpc.setup()

    return mpc
