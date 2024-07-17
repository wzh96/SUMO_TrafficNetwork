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


def MPC_Controller(model, silence_solver = False):
    mpc = do_mpc.controller.MPC(model)

    setup_mpc = {
        'n_horizon': 3,
        't_step': 1,
        'n_robust': 0,
        'store_full_solution': True,
        'nlpsol_opts': {'ipopt.linear_solver': 'mumps', 'ipopt.max_iter': 2000}
    }
    mpc.set_param(**setup_mpc)
    if silence_solver:
        mpc.settings.supress_ipopt_output()

    # set model objective function
    mterm = 1e-5 * (-model._x['x0'] - model._x['x1'] - model._x['x2'] - model._x['x3']
             - model._x['x4'] - model._x['x5'] - model._x['x6'] - model._x['x7'])
    lterm = 1e-5 * (-model._x['x0'] - model._x['x1'] - model._x['x2'] - model._x['x3']
             - model._x['x4'] - model._x['x5'] - model._x['x6'] - model._x['x7'])

    mpc.set_objective(mterm=mterm, lterm=lterm)

    R = 1e-10
    mpc.set_rterm(
        u0=R,
        u1=R,
        u2=R,
        u3=R,
        u4=R,
        u5=R,
        u6=R,
        u7=R
    )

    # state lower bound
    mpc.bounds['lower', '_x', 'x0'] = 1000
    mpc.bounds['lower', '_x', 'x1'] = 1000
    mpc.bounds['lower', '_x', 'x2'] = 1000
    mpc.bounds['lower', '_x', 'x3'] = 1000
    mpc.bounds['lower', '_x', 'x4'] = 1000
    mpc.bounds['lower', '_x', 'x5'] = 1000
    mpc.bounds['lower', '_x', 'x6'] = 1000
    mpc.bounds['lower', '_x', 'x7'] = 1000

    # state upper bound
    mpc.bounds['upper', '_x', 'x0'] = 13000
    mpc.bounds['upper', '_x', 'x1'] = 13000
    mpc.bounds['upper', '_x', 'x2'] = 13000
    mpc.bounds['upper', '_x', 'x3'] = 13000
    mpc.bounds['upper', '_x', 'x4'] = 13000
    mpc.bounds['upper', '_x', 'x5'] = 13000
    mpc.bounds['upper', '_x', 'x6'] = 13000
    mpc.bounds['upper', '_x', 'x7'] = 13000

    # control lower bound
    mpc.bounds['lower', '_u', 'u0'] = 200
    mpc.bounds['lower', '_u', 'u1'] = 200
    mpc.bounds['lower', '_u', 'u2'] = 200
    mpc.bounds['lower', '_u', 'u3'] = 200
    mpc.bounds['lower', '_u', 'u4'] = 200
    mpc.bounds['lower', '_u', 'u5'] = 200
    mpc.bounds['lower', '_u', 'u6'] = 200
    mpc.bounds['lower', '_u', 'u7'] = 200

    # control upper bound
    mpc.bounds['upper', '_u', 'u0'] = 1800
    mpc.bounds['upper', '_u', 'u1'] = 1800
    mpc.bounds['upper', '_u', 'u2'] = 1800
    mpc.bounds['upper', '_u', 'u3'] = 1800
    mpc.bounds['upper', '_u', 'u4'] = 1800
    mpc.bounds['upper', '_u', 'u5'] = 1800
    mpc.bounds['upper', '_u', 'u6'] = 1800
    mpc.bounds['upper', '_u', 'u7'] = 1800


    mpc.setup()

    return mpc
