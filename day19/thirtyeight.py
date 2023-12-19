from math import prod
from typing import List

START = 'in'
ACCEPT = 'A'
REJECT = 'R'


def splitlines(workflows: str) -> List[str]:
    """Split and strip"""
    return [workflow.strip() for workflow in workflows.split('\n')]


def main() -> int:
    """main"""
    with open('test_input.txt', 'r') as f_in:
        workflows, _ = f_in.read().split('\n\n')
    workflows_list = splitlines(workflows)

    workflows = {}
    for workflow in workflows_list:
        workflow_split = workflow.split('{')
        workflows[workflow_split[0]] = []
        conditions = workflow_split[1].split(',')[:-1]
        len_conditions = len(conditions)
        for count, condition in enumerate(conditions):
            workflows[workflow_split[0]].append({
                'category': condition.replace('>', '<').split('<')[0],
                'condition': int(condition.replace('>', '<').split('<')[1].split(':')[0])
                    if '<' in condition
                    else 4000 - int(condition.replace('>', '<').split('<')[1].split(':')[0]),
                True: condition.split(':')[-1],
                False: workflow_split[1].rstrip('}').split(',')[-1] if count == len_conditions - 1 else None,
            })
    import json
    print(json.dumps(workflows, indent=2))

    # Create backward mapping
    total = {}
    outer_workflow_keys = list(workflows.keys())
    outer_workflow_keys.append(ACCEPT)
    for outer_workflow in outer_workflow_keys:
        total[outer_workflow] = {}
        for workflow, conditions in workflows.items():
            total[outer_workflow][workflow] = {category: 0 for category in 'xmas'}
            for condition in conditions:
                if condition.get(True) == outer_workflow:
                    total[outer_workflow][workflow][condition.get('category')] += condition.get('condition')
                if condition.get(False) == outer_workflow:
                    total[outer_workflow][workflow][condition.get('category')] += 4000 - condition.get('condition')
            # if not any(total[outer_workflow][workflow].values()):
            #     total[outer_workflow].pop(workflow)
            to_pop = [key for key, val in total[outer_workflow][workflow].items() if not val]
            for key in to_pop:
                total[outer_workflow][workflow].pop(key)
        to_pop = [key for key, val in total[outer_workflow].items() if not val]
        for key in to_pop:
            total[outer_workflow].pop(key)
        if not total[outer_workflow]:
            total.pop(outer_workflow)  # get rid of START
    # print(json.dumps(total, indent=2))

    # Trying backwards
    sum_val = 0
    for key, val in total.get(ACCEPT).items():
        while key != START:
            # assert len(total.get(inner_key)) == 1
            key, inner_val = list(total.get(key).items())[0]
            for inner_key, parts in inner_val.items():
                val[inner_key] = min(val.get(inner_key, 4000), parts)
            # print(count)
        for category in 'xmas':
            val[category] = val.get(category, 4000)
        print(val)
        sum_val += prod(val.values())
        # print(val, total.get(key))

    # Trying in forward direction
    # all_posib = 0
    # # for key, val in workflows.get(START).items():
    # key = START
    # # all_posib -= workflows[START][0]['condition'] * 4000 ** 3
    # key = workflows[START][0][True]
    # while key != ACCEPT:
    #     all_posib -= 
    # key = workflows[START][0][False]

    return sum_val  # should be 167_409_079_868_000 167409079868000
    #                                               304318042864000
    #                                               256000000000000 - max (4000 ** 4)


if __name__ == '__main__':
    print(main())
