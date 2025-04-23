import argparse
import pytimeloop.timeloopfe.v4 as tl
import re
import yaml
import os


def get_arguments():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--clear-outputs",
        default=False,
        action="store_true",
        help="Clear all generated outputs",
    )
    argparser.add_argument(
        "--architecture",
        type=str,
        default="eyeriss_like",
        help="Architecture to run in the example_designs directory. "
        "If 'all' is given, all architectures will be run.",
    )
    argparser.add_argument(
        "--generate-ref-outputs",
        default=False,
        action="store_true",
        help="Generate reference outputs instead of outputs",
    )
    argparser.add_argument(
        "--problem",
        type=str,
        default=None,
        help="Problem to run in the layer_shapes directory. If a directory is "
        "specified, all problems in the directory will be run. If not specified, "
        "the default problem will be run.",
    )
    argparser.add_argument(
        "--n_jobs", type=int, default=None, help="Number of jobs to run in parallel"
    )
    argparser.add_argument(
        "--remove-sparse-opts",
        default=False,
        action="store_true",
        help="Remove sparse optimizations",
    )
    return argparser.parse_args()


def run_mapper(
    arch_target,
    problem
):
    THIS_SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))    
    EXAMPLE_DIR = os.path.join(THIS_SCRIPT_DIR, "arch")
    TOP_JINJA_PATH = os.path.join(EXAMPLE_DIR, "top.yaml.jinja2")

    # This data will be supplied when rendering the top jinja2 template
    jinja_parse_data = {"architecture": arch_target}

    problem_name = os.path.basename(problem).split(".")[0]
    jinja_parse_data["problem"] = problem

    # Set up output directory
    output_dir = f"{THIS_SCRIPT_DIR}/outputs/{arch_target}/{arch_target}-{problem_name}"

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

def remove_sparse_optimizations(spec: tl.Specification):
    """This function is used by some Sparseloop tutorials to test with/without
    sparse optimizations"""
    for s in spec.get_nodes_of_type(
        (
            tl.sparse_optimizations.ActionOptimizationList,
            tl.sparse_optimizations.RepresentationFormat,
            tl.sparse_optimizations.ComputeOptimization,
        )
    ):
        s.clear()
    return spec

def extract_dram_utilized_capacity(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    in_dram = False
    current_section = None
    intput = 0
    output = 0
    weight = 0
    
    for line in lines:
        line = line.strip()

        # Detect the start of DRAM level
        if line.startswith("=== DRAM ==="):
            in_dram = True
            continue

        # Exit DRAM parsing if another level starts
        if in_dram and line.startswith("===") and not line.startswith("=== DRAM ==="):
            break

        # Identify current section
        if line.startswith("Inputs:"):
            current_section = 'input'
        elif line.startswith("Outputs:"):
            current_section = 'output'
        elif line.startswith("Weights:"):
            current_section = 'weight'

        # Extract Utilized capacity
        if in_dram and "Utilized capacity" in line:
            match = re.search(r'Utilized capacity\s+:\s+([0-9.]+)', line)
            if match and current_section:
                value = float(match.group(1))
                if current_section == 'input':
                    intput = value
                elif current_section == 'output':
                    output = value
                elif current_section == 'weight':
                    weight = value
                
    return [intput, output, weight]

def extract_total_chip_area(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    total_area = 0.0
    for line in lines:
        line = line.strip()
        if line.startswith("Area") and "um^2" in line:
            match = re.search(r'Area\s+\(total\)?\s*:\s*([0-9.]+)', line)
            if not match:
                match = re.search(r'Area\s*:\s*([0-9.]+)', line)
            if match:
                total_area += float(match.group(1))
    return total_area

def extract_total_energy(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Energy:") and "uJ" in line:
            match = re.search(r'Energy:\s+([0-9.]+)\s*uJ', line)
            if match:
                return float(match.group(1))
    return None

def extract_total_cycles(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Cycles:"):
                match = re.search(r"Cycles:\s+([0-9]+)", line)
                if match:
                    return int(match.group(1))
    return None

def search_directories(path):
    directories = []
    for dirpath, dirnames, filenames in os.walk(path):
        directories.append(dirpath)
    return directories

def save_to_yaml(output_path, dram_caps, area, energy, cycles):
    result = {
        'dram_utilized_capacity': dram_caps,
        'total_chip_area_um2': area,
        'total_energy_uJ': energy,
        'total_cycles': cycles
    }

    with open(output_path, 'w') as yaml_file:
        yaml.dump(result, yaml_file, default_flow_style=False)

    