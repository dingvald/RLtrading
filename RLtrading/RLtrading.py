import MarketData as md
import numpy as np
import time
import os
from pathlib import Path
from stable_baselines3 import A2C
from stable_baselines3.common.callbacks import CallbackList
from matplotlib import pyplot as plt
from CustomCallbacks import ProgressBarCallback, ProgressBarManager
import gym
import gym_anytrading


def main():

    # Get data a split into training and testing

    print("Retreiving data...")
    data = md.get_data("HD",period='5y')

    training_data, testing_data = np.split(data, [int(0.8*len(data))])


    training_entries = len(training_data)
    testing_entries = len(testing_data)

    saved_model = Path("../saved_models/a2c_model.zip")

    # Build env and model

    print("Building environment...")
    training_env = gym.make('stocks-v0', df=training_data, frame_bound=(5,training_entries), window_size=5)
    testing_env = gym.make('stocks-v0', df=testing_data, frame_bound=(5,testing_entries), window_size=5)
    training_env.reset()
    print("Building model...")

    if saved_model.is_file():
        print("Loading model...")
        model = A2C.load(saved_model)
        model.set_env(training_env)
    else:
        print("Creating new model...")
        model = A2C('MlpPolicy', training_env)

    # Training phase

    print("Model is learning...")

    time_steps = 1000

    with ProgressBarManager(time_steps) as callback:
        model.learn(total_timesteps=time_steps, callback=callback)

    model.save("../saved_models/a2c_model")


    # Testing phase

    print("Testing Model...")

    testing_runs = 10
    profit = []
    seed_time = int(time.time())
    
    for i in range(testing_runs):

        testing_env.seed(seed_time)
        obs = testing_env.reset()

        p = 0
        for j in range(testing_entries-10):
            action, _states = model.predict(obs)
            obs, rewards, done, info = testing_env.step(action)
            p = info['total_profit']
        profit.append(p)

    print("Testing complete.")
    
    plt.figure(figsize=(12,5))
    plt.scatter(list(range(testing_runs)), profit)
    plt.show()
 

main()