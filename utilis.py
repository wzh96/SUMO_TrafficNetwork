import pysindy as psd

params = {}
params['total_sim_step'] = 14400
params['control_interval'] = 60


MPC_params = {
    'coeff_mterm' : 1,
    'coeff_lterm' : 1,
    'coeff_R' : 0,
    'desire_occu' : 15
}

setup_mpc = {
    'n_horizon': 5,
    't_step': 1,
    'n_robust': 1,
    'store_full_solution': True,
    'nlpsol_opts': {'ipopt.max_iter': 2000}
}

sindy_params = {
    'library' : psd.ConcatLibrary([psd.PolynomialLibrary(degree=2)]),
    'optimizer_threshold' : 2e-4
}