CarbonLoop: A Systematic Modeling of Carbon Emissions in AI Accelerators
======================================

# Instructions
When you want to run CarbonLoop once without sweeping the parameter, follow `Case 1) Run CarbonLoop`. When you want to sweep an architecture parameter and draw the result plots, follow `Case 2) Sweep with CarbonLoop`.

# Case 1) Run CarbonLoop
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

## Expected Results
```
-----------------------------------------------
Total Carbon Footprint    : 0.322267 kg CO2
- Operational CF          : 0.126855 kg CO2
- Discounted Embodied CF  : 0.195412 kg CO2

- Embodied CF             : 0.325686 kg CO2
   - Processor CF         : 0.003573 kg CO2
   - DRAM CF              : 0.022113 kg CO2
   - Package CF           : 0.300000 kg CO2
-----------------------------------------------
```

# Case 2) Sweep with CarbonLoop
In `workspace/3_CarbonLoop`, use the below command to run `run_CarbonLoop_part1.py`. 

```
python3 run_CarbonLoop_part1.py
```

These are the given input as an example task.
* Architecture: Eyeriss-like accelerator with 28 nm technology, with varying global buffer size from 0.5 kB to 1.5 kB
* Workload: Chat-GPT 2

Outputs will be generated in `workspace/3_CarbonLoop/outputs-gb`.

In `workspace/3_CarbonLoop`, run the entire Jupiter notebook of `run_CarbonLoop_part2.py`. The output figures will be generated in `workspace/3_CarbonLoop/figures`


# Authors
Eunseok Lee (eunseok@mit.edu)\
Hyemin Stella Lee (hmstella@mit.edu)

# References
* [ACT: Architectural Carbon Modeling Tool](https://github.com/alugupta/ACT)
* [Timeloop](https://github.com/Accelergy-Project/timeloop-accelergy-exercises)
