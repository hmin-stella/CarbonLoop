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
    ### Run Timeloop-Accelergy across different PE numbers ###
    args = get_arguments()
    args.architecture = 'eyeriss_like'
    pe_list=[]
    for i in range(16,201,4):
        pe_list.append(i)
    args.problem = 'gpt2'
    args.n_jobs = 16

    arch = []
    for pe in pe_list:
        arch.append(args.architecture+'_pe_'+str(pe))

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
            a, p
        )
        for a in arch
        for p in sorted(problems)
    )
