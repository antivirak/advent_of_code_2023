from math import prod
from typing import List

from thirtyseven import splitlines

START = 'in'
ACCEPT = 'A'
REJECT = 'R'


class LenFourThousand:
    """Hacky class to get 4000 as len of arbitrary object"""
    def __len__(self):
        return 4000


def main() -> int:
    """main"""
    with open('input.txt', 'r') as f_in:
        workflows, _ = f_in.read().split('\n\n')
    workflows_list = splitlines(workflows)

    workflows = {}
    skip = []
    for workflow in workflows_list:
        workflow_split = workflow.split('{')
        workflows[workflow_split[0]] = []
        conditions = workflow_split[1].split(',')[:-1]
        len_conditions = len(conditions)
        for count, condition in enumerate(conditions):
            true = condition.split(':')[-1]
            false = workflow_split[1].rstrip('}').split(',')[-1]
            if true == false and true == ACCEPT:
                skip.append(workflow_split[0])
                continue
            workflows[workflow_split[0]].append({
                'category': condition.replace('>', '<').split('<')[0],
                'condition': range(
                    1, int(condition.replace('>', '<').split('<')[1].split(':')[0])
                ) if '<' in condition else range(
                    int(condition.replace('>', '<').split('<')[1].split(':')[0]) + 1, 4001,
                ),
                True: true,
                False: false if count == len_conditions - 1 else None,
            })
    print(skip)
    for workflow, conditions in workflows.items():
        for cond in conditions:
            print(cond)
            if cond.get(True) in skip:
                cond[True] = ACCEPT
            if cond.get(False) in skip:
                cond[False] = ACCEPT
    # print(json.dumps(workflows, indent=2))

    # Create backward mapping
    total = {}
    outer_workflow_keys = list(workflows.keys())
    outer_workflow_keys.append(ACCEPT)
    for outer_workflow in outer_workflow_keys:
        total[outer_workflow] = {}
        for workflow, conditions in workflows.items():
            total[outer_workflow][workflow] = {category: set() for category in 'xmas'}
            # adding condition key
            total[outer_workflow][workflow]['condition'] = {}
            for condition in conditions:
                if condition.get(True) == outer_workflow:
                    total[outer_workflow][workflow][condition.get('category')].update(condition.get('condition'))
                elif condition.get(False) is None:
                    to_update = set(range(1, 4001)) - set(condition.get('condition'))
                    # if not total[outer_workflow][workflow]['condition'].get(condition.get('category')):
                    total[outer_workflow][workflow]['condition'][condition.get('category')] = to_update
                    # else:
                    #     total[outer_workflow][workflow]['condition'][condition.get('category')].update(to_update)
                if condition.get(False) == outer_workflow:
                    to_update = set(range(1, 4001)) - set(condition.get('condition'))
                    total[outer_workflow][workflow][condition.get('category')].update(to_update)  # set(range(1, 4001)) - set(condition.get('condition'))
                # for print:
                # total[outer_workflow][workflow][condition.get('category')] = (min(total[outer_workflow][workflow][condition.get('category')] or [0]), max(total[outer_workflow][workflow][condition.get('category')] or [0]))
                # total[outer_workflow][workflow]['condition'][condition.get('category')] = (min(total[outer_workflow][workflow]['condition'].get(condition.get('category')) or [0]), max(total[outer_workflow][workflow]['condition'].get(condition.get('category')) or [0]))
                # if total[outer_workflow][workflow][condition.get('category')] == (0, 0):
                #     total[outer_workflow][workflow][condition.get('category')] = None
                # if total[outer_workflow][workflow]['condition'][condition.get('category')] == (0, 0):
                #     total[outer_workflow][workflow]['condition'].pop(condition.get('category'))
            # if not any(total[outer_workflow][workflow].values()):
            #     total[outer_workflow].pop(workflow)
            if not total[outer_workflow][workflow]['condition']:
                total[outer_workflow][workflow].pop('condition')
            total_workflow_key = total[outer_workflow][workflow].keys()
            to_pop = [key for key, val in total[outer_workflow][workflow].items() if not val]
            for key in to_pop:
                total[outer_workflow][workflow].pop(key)
            if 'condition' in total_workflow_key and len(total_workflow_key) == 1:
                total[outer_workflow][workflow].pop('condition')
        to_pop = [key for key, val in total[outer_workflow].items() if not val]
        for key in to_pop:
            total[outer_workflow].pop(key)
        if not total[outer_workflow]:
            total.pop(outer_workflow)  # get rid of START
    # print(json.dumps(total, indent=2))

    # search backwards from each ACCEPT to START
    sum_val = 0
    for key, val in total.get(ACCEPT).items():
        while key != START:
            # print(list(total.get(key).keys()))
            if not total.get(key):
                break
            assert len(total.get(key)) == 1
            # print(key)
            key, inner_val = [(key_, val_) for key_, val_ in total.get(key).items()][0]  #  if 'condition' not in val_.keys()
            for inner_key, parts in inner_val.items():
                if inner_key == 'condition':
                    continue
                # print(inner_key, len(val.get(inner_key, [])), len(parts))
                for category_key, category_val in inner_val.get('condition', {}).items():
                    # print(category_key, len(val.get(category_key, [])), min(category_val), max(category_val))
                    # if category_key in val.keys():
                    intersect = val.get(category_key, set(range(1, 4001))).intersection(category_val)
                    if intersect:
                        val[category_key] = intersect  # .intersection(val.get(inner_key, set(range(1, 4001))))
                val[inner_key] = val.get(inner_key, parts).intersection(parts)  # .intersection(val.get('condition', {}).get(inner_key, set(range(1, 4001))))
            # print(count)
        for category in 'xmas':
            # print('last loop', category, len(val.get(category, [])), len(val.get('condition', {}).get(category, [])))
            val[category] = val.get(category, set(range(1, 4001))).intersection(val.get('condition', {}).get(category, set(range(1, 4001))))
            val[category] = len(val[category])
            # val[category] = len(val.get(category, LenFourThousand()))
        # print({_: __ for _, __ in val.items() if _ != 'condition'}, prod(value for value in val.values() if isinstance(value, int)))
        # print()
        sum_val += prod(value for value in val.values() if isinstance(value, int))

    return sum_val  # 79931050367370 incorrect


if __name__ == '__main__':
    print(main())
