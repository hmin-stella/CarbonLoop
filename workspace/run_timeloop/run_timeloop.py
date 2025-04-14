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

def run_mapper(
    arch_target,
    problem: Optional[str] = None,
):
    # This data will be supplied when rendering the top jinja2 template
    jinja_parse_data = {"architecture": arch_target}

    problem_name = os.path.basename(problem).split(".")[0]
    jinja_parse_data["problem"] = problem

    # Set up output directory
    output_dir = f"{THIS_SCRIPT_DIR}/outputs/{arch_target}-{problem_name}"

    print(f"\n\nRunning mapper for target {arch_target} in {output_dir}...")

    # Set up output directory
    if os.path.exists(output_dir):
        os.system(f"rm -rf {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    spec = tl.Specification.from_yaml_files(
        TOP_JINJA_PATH, jinja_parse_data=jinja_parse_data
    )

    tl.call_mapper(spec, output_dir=output_dir, dump_intermediate_to=output_dir)
    assert os.path.exists(f"{output_dir}/timeloop-mapper.stats.txt"), (
        f"Mapper did not generate expected output for {arch_target}. "
        f"Please check the logs for more details."
    )


if __name__ == "__main__":
    args = get_arguments()
    args.architecture = 'eyeriss_like'
    args.problem = 'gpt2'

    arch = args.architecture

    # Default to the first architecture if none is specified
    if arch is None or not arch:
        arch = arch_targets[0]
    # If arch is "all", run all architectures
    if str(arch).lower() == "all":
        arch = arch_targets

    # If arch is a string, make it a list
    arch = [arch] if isinstance(arch, str) else arch

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
