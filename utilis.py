import pysindy as psd

params = {}
params['total_sim_step'] = 7200
params['control_interval'] = 120


MPC_params = {
    'param_mterm' : 1,
    'param_lterm' : 1,
    'param_R' : 0,
    'desire_occu' : 25,
    'param_U_upper': 180,
    'param_U_lower': 20,
    'param_X_upper': 80,
    'param_X_lower': 0
}

setup_mpc = {
    'n_horizon': 3,
    't_step': 1,
    'n_robust': 0,
    'store_full_solution': True,
    'nlpsol_opts': {'ipopt.max_iter': 2000}
}

sindy_params = {
    'library' : psd.ConcatLibrary([psd.PolynomialLibrary(degree=2)]),
    'optimizer_threshold' : 2e-4
}