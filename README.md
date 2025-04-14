Carbon Footprint Modeling with Hardware Design Space Exploration
======================================

# Instructions

In the `workspace` directory, you will go through directories of `1_run_timeloop` and `2_integrate_with_act` to generate the carbon footprint of an example architecture and workload.

## Step 1: Run Timeloop
In `workspace/1_run_timeloop`, use the below command to run `run_timeloop.py`. 

```
python3 run_timeloop.py
```

These are the given input as an example task.
* Architecture: **Eyeriss-like accelerator** with 28 nm technology
* Workload: **Chat-GPT 2**

Outputs will be generated in `workspace/1_run_timeloop/outputs`.

## Step 2: Run ACT
In `workspace/2_integrate_with_act`, run the entire Jupiter notebooks listed below in order.
* `m00_time-loop_extract.ipynb`
* `m01_integrate_with_act.ipynb`

`moo_time-loop_extract.ipynb` reads the output of Timeloop generated in Step 1, and generates `timeloop_summary.yaml`, a file including parameters that will be transferred from Timeloop output to ACT input.

Finally, `m01_integrate_with_act.ipynb` generates the carbon footprint of the example task.


# Authors
Eunseok Lee (eunseok@mit.edu)\
Hyemin Stella Lee (hmstella@mit.edu)
