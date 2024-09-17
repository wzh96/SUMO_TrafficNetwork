import pysindy as psd

params = {}
params['total_sim_step'] = 7200
params['control_interval'] = 120
params['burnin_step'] = 1800
params['cool_down_step'] = 900

ALINEA_params = {
    'desire_occu' : 15,
    'K_P' : 70, # for PI-ALINEA
    'K_R' : 70,
    'K_F' : 1, # for FL-ALINEA
    'r_min': 200,
    'r_max': 1800,
    'desire_flow_lane': 1800 * 0.8 # for FL_ALINEA
}

MPC_params = {
    'param_mterm' : 1,
    'param_lterm' : 1,
    'param_R' : 0,
    'desire_occu' : 15,
    'param_U_upper': 180,
    'param_U_lower': 20,
    'param_X_upper': 80,
    'param_X_lower': 0
}

setup_mpc = {
    'n_horizon': 5,
    't_step': 1,
    'n_robust': 0,
    'store_full_solution': True,
    'nlpsol_opts': {'ipopt.max_iter': 2000}
}

sindy_params = {
    'library' : psd.ConcatLibrary([psd.PolynomialLibrary(degree=2)]),
    'optimizer_threshold' : 2e-4
}