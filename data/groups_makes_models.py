import json

with open(r".\data\makes_groups.json", "r") as f:
    makes_groups = json.load(f)

groups = {group_name: f"{group_id+1:03}" for group_id, group_name in enumerate(set(makes_groups[make] for make in makes_groups))}
groups_makes_models = {}
for make_name in makes_groups:
    group_name = makes_groups.get(make_name)
    group_id = groups.get(group_name)
    if group_name in groups_makes_models:
        make_id = f"{group_id}-{len(groups_makes_models[group_name]['makes']) + 1:03}"
        groups_makes_models[group_name]["makes"][make_name] = dict(makeId=make_id, models={})
    else:
        make_id = f"{group_id}-001"
        groups_makes_models[group_name] = dict(groupId=group_id, makes={make_name: dict(makeId=make_id, models={})})

# Populate groups_makes_models dict with models
with open(r".\data\models.json", "r") as f:
    vehicles_json = json.load(f)

vehicles = vehicles_json.get("results")
for vehicle in vehicles:
    model_name = vehicle.get("Model")
    model_id = vehicle.get("objectId")
    make_name = vehicle.get("Make").title() if len(vehicle.get("Make")) > 3 else vehicle.get("Make")
    group_name = makes_groups.get(make_name)
    group = groups_makes_models.get(group_name)
    if group:
        if make_name in group.get("makes"):
            make = group.get("makes").get(make_name)
            make_id = make.get("makeId")
            groups_makes_models[group_name]["makes"][make_name]["models"][model_name] = f"{make_id}-{model_id}"

# Delete makes with no models
del_groups = []
del_makes = {}
for group_name in groups_makes_models:
    group = groups_makes_models.get(group_name)
    makes = group.get("makes")
    for make_name in makes:
        make = makes.get(make_name)
        if not make.get("models"):
            if len(makes) > 1:
                del_makes[group_name] = make_name
            else:
                del_groups.append(group_name)

[groups_makes_models.pop(group_name) for group_name in del_groups]
[groups_makes_models.get(group_name).get("makes").pop(make_name) for group_name, make_name in del_makes.items()]

with open(r".\data\groups_makes_models.json", "w") as f:
    json.dump(groups_makes_models, f, indent=6)
