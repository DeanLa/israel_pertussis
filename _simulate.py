if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import gaussian_kde as kde
    # from scipy.stats import norm, uniform, multivariate_normal as multinorm, norm
    # from tqdm import tqdm
    import seaborn as sns

    np.set_printoptions(edgeitems=10, linewidth=120, suppress=True, precision=8)

    from pertussis import *

    logger.setLevel(logging.INFO)

    # load = False
    load = False
    if load:
        # load simulation
        simulation = load_mcmc('./simulations/rho-60-36k.pkl')
        mcmc = simulation['mcmc']
        print(simulation['name'])
        print(len(simulation['p']))
        print(mcmc['name'])
        print(len(mcmc['chain']))
        print(mcmc['tally'])
    else:
        # Load MCMC
        mcmc = load_mcmc('./chains/mcmc_imoh.pkl')
        print(mcmc['name'], ': ', len(mcmc['chain']))
        print(mcmc['tally'])
        names = mcmc['names']
        # Take subsets
        take_subsets(mcmc)
        # Create Policies
        default = init_policy('default')
        # everybody = init_policy('everybody', vax_ages=a_l)
        # no_one = init_policy('no_one', vax_ages=[])

        # possible_ages = [5,6,7,8,9,10,11,12,13,15,18]

        policies = [default]

        # No boosters
        p_name = 'No Boosters'
        tmp_ages = (a_l[0], a_l[1], a_l[2], a_l[5])
        tmp_policy = init_policy(p_name, vax_ages=tmp_ages)
        policies.append(tmp_policy)
        # Remove
        # only_age = [5,6,7,10,13]
        only_age = [4, 5, 6, 12]
        for age in only_age:
            p_name = '{:02d}'.format(age + 1)
            tmp_ages = (a_l[0], a_l[1], a_l[2], a_l[5], age)
            tmp_policy = init_policy(p_name, vax_ages=tmp_ages)
            policies.append(tmp_policy)

        # Shift
        possible_ages = [4, 5, 6, 7, 12]
        # possible_ages = [5,7,13]
        for i in range(len(possible_ages)):
            for j in range(i):

                agej, agei = possible_ages[j], possible_ages[i]
                if (agej == 6) and (agei == 12): continue
                p_name = '{:02d},{:02d}'.format(agej + 1, agei + 1)
                tmp_ages = (a_l[0], a_l[1], a_l[2], a_l[5], agej, agei)
                tmp_policy = init_policy(p_name, vax_ages=tmp_ages)
                policies.append(tmp_policy)

        # Add
        additional_ages = [7, 8, 13]
        # additional_ages = [5]
        for age in additional_ages:
            p_name = '05,{:02d},13'.format(age + 1)
            tmp_ages = (a_l[0], a_l[1], a_l[2], a_l[5], 4, 12, age)
            tmp_policy = init_policy(p_name, vax_ages=tmp_ages)
            policies.append(tmp_policy)
        # Create the simulation

        print(len(policies))
        simulation = init_simulation("1706-imoh-qaly", mcmc, policies)
        simulation.keys()
        # [p['name'] for p in policies]

        simulate_future(simulation, 2000)
