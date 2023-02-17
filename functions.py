import numpy as np


def generate_trials(angles, reps, type="forced"):
    angles = np.array(angles).flatten()
    if type == "forced":
        conds = np.concatenate([np.zeros(angles.shape), np.ones(angles.shape)])
        angles = np.tile(angles, 2)
        conditions = np.vstack([angles, conds]).transpose()
        order = np.tile(np.arange(conditions.shape[0]), reps)

        while True:
            np.random.shuffle(order)
            if np.mean(order[1:] == order[:-1]) == 0:
                break
        
        conditions = np.vstack([conditions[i] for i in order])
        return conditions

    if type == "free":
        conditions = np.tile(angles, reps)
        
        while True:
            np.random.shuffle(conditions)
            if np.mean(conditions[1:] == conditions[:-1]) == 0:
                break

        return conditions

