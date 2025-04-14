
# Copyright (c) Meta Platforms, Inc. and affiliates.

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import sys


class Fab_Logic():
    def __init__(self, process_node=14,
                       gpa="97",
                       fab_carbon_intensity="loc_taiwan",
                       use_carbon_intensity="loc_usa",
                       debug=False,
                       fab_yield=0.875):

        self.debug = debug

        ###############################
        # Energy per unit area
        ###############################
        with open("/home/workspace/ACT-tutorial/logic/epa.json", 'r') as f:
            epa_config = json.load(f)

        ###############################
        # Raw materials per unit area
        ###############################
        with open("/home/workspace/ACT-tutorial/logic/materials.json", 'r') as f:
            materials_config = json.load(f)

        ###############################
        # Gasses per unit area
        ###############################
        if gpa == "95":
            with open("/home/workspace/ACT-tutorial/logic/gpa_95.json", 'r') as f:
                gpa_config = json.load(f)

        elif gpa == "99":
            with open("/home/workspace/ACT-tutorial/logic/gpa_99.json", 'r') as f:
                gpa_config = json.load(f)

        elif gpa == "97":
            with open("/home/workspace/ACT-tutorial/logic/gpa_95.json", 'r') as f:
                gpa_95_config = json.load(f)
            with open("/home/workspace/ACT-tutorial/logic/gpa_99.json", 'r') as f:
                gpa_99_config = json.load(f)

            gpa_config = {}
            for c in gpa_95_config.keys():
                gas = (gpa_95_config[c] + gpa_99_config[c]) / 2.
                gpa_config[c] = gas

        else:
            print("Error: Unsupported GPA value for FAB logic")
            sys.exit()

        ###############################
        # Carbon intensity of fab
        ###############################
        if "loc" in fab_carbon_intensity:
            with open("/home/workspace/ACT-tutorial/carbon_intensity/location.json", 'r') as f:
                loc_configs = json.load(f)

                loc = fab_carbon_intensity.replace("loc_", "")

                assert loc in loc_configs.keys()

                fab_ci = loc_configs[loc]

        elif "src" in fab_carbon_intensity:
            with open("/home/workspace/ACT-tutorial/carbon_intensity/source.json", 'r') as f:
                src_configs = json.load(f)

                src = fab_carbon_intensity.replace("src_", "")

                assert src in src_configs.keys()

                fab_ci = src_configs[src]

        else:
            print("Error: Carbon intensity must either be loc | src dependent")
            sys.exit()


        ###############################
        # Carbon intensity of user
        ###############################
        with open("/home/workspace/ACT-tutorial/carbon_intensity/location.json", 'r') as f:
            loc_configs = json.load(f)
            loc = use_carbon_intensity.replace("loc_", "")
            self.use_ci = loc_configs[loc]

        ###############################
        # Aggregating model
        ###############################
        process_node = str(process_node) + "nm"
        assert process_node in epa_config.keys()
        assert process_node in gpa_config.keys()
        assert process_node in materials_config.keys()

        carbon_energy    = fab_ci * epa_config[process_node]
        carbon_gas       = gpa_config[process_node]
        carbon_materials = materials_config[process_node]

        self.carbon_per_area = (carbon_energy + carbon_gas + carbon_materials)
        self.carbon_per_area = self.carbon_per_area / fab_yield

        if self.debug:
            print("[Fab logic] Carbon/area from energy consumed" , carbon_energy)
            print("[Fab logic] Carbon/area from gasses"          , carbon_gas)
            print("[Fab logic] Carbon/area from materials"       , carbon_materials)
            print("[Fab logic] Carbon/area aggregate"            , self.carbon_per_area)

        self.carbon = 0

        return


    def get_cpa(self,):
        return self.carbon_per_area

    def set_area(self, area):
        self.area = area
        self.carbon = self.area * self.carbon_per_area

    def get_carbon(self, ):
        return self.carbon

    def get_use_ci(self, ):
        return self.use_ci
