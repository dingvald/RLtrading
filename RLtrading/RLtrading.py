import MarketData as md
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
    print("Retreiving data...")
    data = md.get_data("HD",period='5y')
    entries = len(data)
    print(entries,"entries in the stock data.")

    saved_model = Path("../saved_models/a2c_model.zip")


    print("Building environment...")
    env = gym.make('stocks-v0', df=data, frame_bound=(5,entries), window_size=5)
    env.reset()
    print("Building model...")

    if saved_model.is_file():
        print("Loading model...")
        model = A2C.load(saved_model)
        model.set_env(env)
    else:
        print("Creating new model...")
        model = A2C('MlpPolicy', env)


    print("shh, model is learning...")

    time_steps = 1000

    start_time = time.perf_counter()
    with ProgressBarManager(time_steps) as callback:
        model.learn(total_timesteps=time_steps, callback=callback)
    end_time = time.perf_counter()
    print("")
    print("Learning complete. It took","{:.2f}".format(end_time - start_time), "seconds.")

    model.save("../saved_models/a2c_model")
    
    plt.figure(figsize=(15,6))
    plt.cla()
    env.render_all()
    plt.show()
    
 

main()