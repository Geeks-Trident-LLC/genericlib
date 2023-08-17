from yaml import safe_load
from pathlib import Path
from pathlib import PurePath
from genericlib import DotObject


def create_ref_pattern():
    file_name = str(PurePath(Path(__file__).parent, 'ref_pattern.yaml'))
    obj = safe_load(open(file_name))
    ref_pattern = DotObject()
    for key, value in obj.items():
        if key in ['date', 'time', 'datetime']:
            for sub_key, sub_val in value.items():
                if sub_key.startswith('format'):
                    new_key = sub_key.replace('format', key)
                    ref_pattern.update({new_key: sub_val})
        else:
            ref_pattern.update({key: value.get('pattern')})
    return ref_pattern


REF_PATTERN = create_ref_pattern()

