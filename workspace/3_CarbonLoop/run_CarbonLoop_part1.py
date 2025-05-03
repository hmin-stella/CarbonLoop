from typing import Optional
import os
import threading
import pytimeloop.timeloopfe.v4 as tl
from util_functions import *
import joblib

Specification = tl.Specification
THIS_SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
EXAMPLE_DIR = os.path.join(THIS_SCRIPT_DIR, "arch")
TOP_JINJA_PATH = os.path.join(EXAMPLE_DIR, "top.yaml.jinja2")


if __name__ == "__main__":
    ### Run Timeloop-Accelergy ###
    ## USER INPUT ##
    args = get_arguments()
    args.architecture = 'eyeriss_like'
    mode = 'pe'
    sweep_list = [56]
    args.problem = 'gpt2'
    ################
    
    arch = []
    for sweep in sweep_list:
        arch.append(args.architecture+'_'+mode+'_'+str(sweep))
    args.n_jobs = 16
    
    # Put togher the list of problems to run
    problems = [None]
    if args.problem:
        problem = os.path.join(THIS_SCRIPT_DIR, "prob", args.problem)
        if os.path.isdir(problem):
            problems = [
                os.path.join(problem, f)
                for f in os.listdir(problem)
                if f.endswith(".yaml")
            ]
        else:
            problems = [problem]

    # Run parallel processes for all architectures and problems
    joblib.Parallel(n_jobs=args.n_jobs)(
        joblib.delayed(run_mapper)(
            a, p, 'outputs-'+mode
        )
        for a in arch
        for p in sorted(problems)
    )
