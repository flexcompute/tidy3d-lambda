def sweep_rerun_pyscript(simulationString, pyscriptDataArrayString, currentParamValue):  # include user python script and gui variable and medium
    import json
    import tidy3d as td
    from types import SimpleNamespace
    simulation = json.loads(simulationString)
    data2 = json.loads(pyscriptDataArrayString)
    print(currentParamValue)
    print(type(currentParamValue))
    for scriptData in data2:
        dependenceParam = scriptData.get('dependenceParam')
        generatedObjectNames = scriptData.get('generatedObjectNames')
        # delete old objects
        def findIndex(flist, func):
            for i,v in enumerate(flist):
                if func(v): return i
            return -1
        for objName in generatedObjectNames:
            index = findIndex(simulation["structures"], lambda v: v["name"] == objName )
            if index > -1:
                del simulation["structures"][index]
                continue
            index = findIndex(simulation["sources"], lambda v: v["name"] == objName )
            if index > -1:
                del simulation["sources"][index]
            index = findIndex(simulation["monitors"], lambda v: v["name"] == objName )
            if index > -1:
                del simulation["monitors"][index]
        # generate new objects
        param = SimpleNamespace(medium = SimpleNamespace())
        for key in dependenceParam:
            if key == 'medium':
                for key2 in dependenceParam[key]:
                    setattr(param.medium, key2, getattr(td, dependenceParam[key][key2].get('type'))(**dependenceParam[key][key2]))
            else:
                setattr(param, key, dependenceParam[key])
        # replace sweep param value
        for key in currentParamValue:
            if key in param:
                param[key] = currentParamValue[key]
        print(param)
        script = scriptData.get('userString') 
        from tidy3d_lambda.script_engine import ScriptEngine
        engine = ScriptEngine("", script=script)
        context = engine.compile()
        context.params = [param]
        result = engine.exec(context)
        # push new objects
        for obj in result:
            if 'Structure' in obj.type:
                simulation["structures"].append(json.loads(obj._json_string))
                continue 
            if 'Source' in obj.type:
                simulation["sources"].append(json.loads(obj._json_string))
                continue 
            if 'Monitor' in obj.type:
                simulation["monitors"].append(json.loads(obj._json_string))
                continue 
        
        print('fff', json.dumps(simulation))

sweep_rerun_pyscript(\
'{"type":"Simulation","center":[0.0,0.0,0.0],"size":[4.0,4.0,4.0],"run_time":4.002769140628792e-13,"medium":{"name":null,"frequency_range":null,"type":"Medium","permittivity":1.0,"conductivity":0.0},"symmetry":[0,0,0],"structures":[{"geometry":{"type":"Box","center":[0.0,0.0,0.0],"size":[1.5,1.5,1.5]},"name":"test","type":"Structure","medium":{"name":null,"frequency_range":null,"type":"Medium","permittivity":4.0,"conductivity":0.0}}],"sources":[{"type":"UniformCurrentSource","center":[-1.5,0.0,0.0],"size":[0.0,0.4,0.4],"source_time":{"amplitude":1.0,"phase":0.0,"type":"GaussianPulse","freq0":299792458130996.0,"fwidth":29979245813099.6,"offset":5.0},"name":"oldSource","polarization":"Ey"}],"boundary_spec":{"x":{"plus":{"name":null,"type":"PML","num_layers":12,"parameters":{"sigma_order":3,"sigma_min":0.0,"sigma_max":1.5,"type":"PMLParams","kappa_order":3,"kappa_min":1.0,"kappa_max":3.0,"alpha_order":1,"alpha_min":0.0,"alpha_max":0.0}},"minus":{"name":null,"type":"PML","num_layers":12,"parameters":{"sigma_order":3,"sigma_min":0.0,"sigma_max":1.5,"type":"PMLParams","kappa_order":3,"kappa_min":1.0,"kappa_max":3.0,"alpha_order":1,"alpha_min":0.0,"alpha_max":0.0}},"type":"Boundary"},"y":{"plus":{"name":null,"type":"PML","num_layers":12,"parameters":{"sigma_order":3,"sigma_min":0.0,"sigma_max":1.5,"type":"PMLParams","kappa_order":3,"kappa_min":1.0,"kappa_max":3.0,"alpha_order":1,"alpha_min":0.0,"alpha_max":0.0}},"minus":{"name":null,"type":"PML","num_layers":12,"parameters":{"sigma_order":3,"sigma_min":0.0,"sigma_max":1.5,"type":"PMLParams","kappa_order":3,"kappa_min":1.0,"kappa_max":3.0,"alpha_order":1,"alpha_min":0.0,"alpha_max":0.0}},"type":"Boundary"},"z":{"plus":{"name":null,"type":"PML","num_layers":12,"parameters":{"sigma_order":3,"sigma_min":0.0,"sigma_max":1.5,"type":"PMLParams","kappa_order":3,"kappa_min":1.0,"kappa_max":3.0,"alpha_order":1,"alpha_min":0.0,"alpha_max":0.0}},"minus":{"name":null,"type":"PML","num_layers":12,"parameters":{"sigma_order":3,"sigma_min":0.0,"sigma_max":1.5,"type":"PMLParams","kappa_order":3,"kappa_min":1.0,"kappa_max":3.0,"alpha_order":1,"alpha_min":0.0,"alpha_max":0.0}},"type":"Boundary"},"type":"BoundarySpec"},"monitors":[{"type":"FieldMonitor","center":[0.0,0.0,0.0],"size":["Infinity","Infinity",0.0],"name":"fields_on_plane","freqs":[299792458130996.0],"apodization":{"start":null,"end":null,"width":null,"type":"ApodizationSpec"},"fields":["Ex","Ey","Hz"],"interval_space":[1,1,1],"colocate":false}],"grid_spec":{"grid_x":{"type":"AutoGrid","min_steps_per_wvl":30.0,"max_scale":1.4,"dl_min":0.0,"mesher":{"type":"GradedMesher"}},"grid_y":{"type":"AutoGrid","min_steps_per_wvl":30.0,"max_scale":1.4,"dl_min":0.0,"mesher":{"type":"GradedMesher"}},"grid_z":{"type":"AutoGrid","min_steps_per_wvl":30.0,"max_scale":1.4,"dl_min":0.0,"mesher":{"type":"GradedMesher"}},"wavelength":null,"override_structures":[],"type":"GridSpec"},"shutoff":1e-5,"subpixel":true,"normalize_index":0,"courant":0.99,"version":"1.9.3"}',\
'[{"userString": "import numpy as np\\nfrom tidy3d_lambda import entrypoint\\nimport tidy3d as td\\n@entrypoint\\ndef generate_object(param):\\n    lambda0 = 1.0\\n    freq0 = td.C_0 / lambda0\\n    fwidth = freq0 / 10.0\\n    square = td.Structure(geometry=td.Box(center=(0, 0, 0), size=(1.5, 1.5, 1.5)), medium=td.Medium.from_nk(n=2, k=0, freq=param.c), name=\\"newTestStructure\\")\\n    return [square, td.UniformCurrentSource(center=(-1.5, 0, 0),size=(0, 0.4, 0.4),source_time=td.GaussianPulse(freq0=freq0, fwidth=fwidth),polarization=\\"Ey\\",name=\\"newTestSource\\")]",\
"generatedObjectNames": ["test", "oldSource"],\
"dependenceParam": {"testParam": 1, "testParam": 2 ,"c":299792458000000,"inf":"Infinity"}}]',
{"testParam1": 11, "testParam2": 22}
)
