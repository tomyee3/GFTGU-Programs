"""
main.py

Entry point for the Random Walk program.
Users may modify maxSteps and nTrials here.
"""

from random_driver import run_random_walk_experiments
from random_plot import plot_random_walk_results

def main():
    # Example parameters (user may overwrite)
    maxSteps = 4096     # analogous to Schutz's default large walk
    nTrials  = 2000     # number of repeated walks for averaging

    lengths, avgDist = run_random_walk_experiments(maxSteps, nTrials)

    plot_random_walk_results(lengths, avgDist)

if __name__ == "__main__":
    main()
