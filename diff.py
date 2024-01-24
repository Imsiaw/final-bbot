import pandas as pd
import os
from datetime import datetime

# ------------------------------------------------------------


bbot_path = "bbot"

diff_path = "diff"


directories = [
    d for d in os.listdir(bbot_path) if os.path.isdir(os.path.join(bbot_path, d))
]

files = []


for dir in directories:
    path = f"{bbot_path}/{dir}"
    sub_dirs = [
        d
        for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
        and "asset-inventory.csv" in os.listdir(f"{path}/{d}")
    ]
    files.append({"label": dir, "children": sub_dirs})


def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


create_dir_if_not_exist(bbot_path)
create_dir_if_not_exist(diff_path)


def diff(obj1, obj2):
    # print(obj1, obj2)
    diff_list = []
    diff_obj = {}
    for item1 in obj1:
        is_diff = False
        for item2 in obj2:
            if item1 == item2:
                diff_obj[item1] = obj1[item1]

                if obj1[item1] != obj2[item1]:
                    is_diff = True
                    diff_obj[item1] = f"{obj1[item1]} => {obj2[item1]}"
                    print(f"found diff! {item1} old {obj1[item1]}  new {obj2[item1]}")
        if is_diff:
            diff_list.append(diff_obj)
    return diff_list


for dir in files:
    date_list = dir["children"]
    date_list = sorted(
        date_list, key=lambda x: datetime.strptime(x, "%Y_%m_%d_%H%M%S"), reverse=True
    )
    label = dir["label"]
    base_path = f"bbot/{label}"

    df1 = (
        pd.read_csv(f"{base_path}/{date_list[1]}/asset-inventory.csv")
        .fillna(value="")
        .to_dict("records")
    )
    df2 = (
        pd.read_csv(f"{base_path}/{date_list[0]}/asset-inventory.csv")
        .fillna(value="")
        .to_dict("records")
    )

    new_items = []
    diff_list = []
    print("----------------")

    for new_item in df2:
        new_host = new_item["Host"]
        is_new = False
        for old_item in df1:
            old_host = old_item["Host"]
            if new_host == old_host:
                is_new = True
                diffed = diff(old_item, new_item)
                if len(diffed) != 0:
                    diff_list.append(*diffed)
        if not is_new:
            new_items.append(new_item)
    final_diff = diff_list + new_items
    if len(final_diff) != 0:
        parent_dir = os.path.join(diff_path, label)
        filename = f'diff_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        file_path = os.path.join(parent_dir, filename)
        create_dir_if_not_exist(parent_dir)
        df = pd.DataFrame(final_diff)
        df.to_csv(file_path, index=False)
