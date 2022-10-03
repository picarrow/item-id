import json
import math
import os
import shutil

# c = x * ceil(log_x(n))
# c = # of predicate checks
# n = # of items
# x = partition size
# the best x minimizes c
PARTITION_SIZE = 3

def partition(lst, d):
    """
    Partitions a list into d similarly sized partitions
    """
    if d <= 0:
        return lst
    p = math.ceil(len(lst) / d)
    return [lst[:p]] + partition(lst[p:], d - 1)

def generate_namespace(tags):
    shutil.rmtree('picarrow.item_id', ignore_errors=True)
    shutil.copytree('data', 'picarrow.item_id')
    items = list(tags.keys())
    generate_lookup_file(items)
    generate_predicates(items)
    generate_assign_functions(tags)
    generate_search_tree_functions(items)

def generate_lookup_file(items):    
    with open('picarrow.item_id/lookup.txt', 'w') as f:
        for i, item in enumerate(items):
            f.write('{0} {1}\n'.format(i + 1, item))

def generate_predicates(items):
    def inner(old_file_name, old_items):
        for i, new_items in enumerate(partition(old_items, PARTITION_SIZE)):
            new_file_name = old_file_name + str(i + 1)
            if len(new_items) >= 1:
                create_predicate(new_file_name, new_items)
            if len(new_items) >= 2:
                inner(new_file_name, new_items)
    inner('0', items)

def generate_assign_functions(tags):
    for i, item in enumerate(items):
        text = 'scoreboard players set @s picarrow.iid.item_id {0}\n'.format(i + 1)
        for tag in tags[item]:
            text += 'tag @s add picarrow.iid.{0}\n'.format(tag)
        file = 'minecraft_' + item.removeprefix('minecraft:')
        path = 'picarrow.item_id/functions/assign/{0}.mcfunction'.format(file)
        with open(path, 'w') as f:
            f.write(text)

def generate_search_tree_functions(items):
    def inner(file_name, items):
        text = ''
        for i, p in enumerate(partition(items, PARTITION_SIZE)):
            predicate_name = file_name + str(i + 1)
            if len(p) >= 2:
                text += 'execute if predicate picarrow.item_id:{0} run function picarrow.item_id:search_tree/{0}\n'.format(predicate_name)
                inner(predicate_name, p)
            elif len(p) == 1:
                assign_function_name = 'minecraft_' + p[0].removeprefix('minecraft:')
                text += 'execute if predicate picarrow.item_id:{0} as @e[type=item,tag=picarrow.iid.assessing,distance=..0.00001] run function picarrow.item_id:assign/{1}\n'.format(predicate_name, assign_function_name)
        create_search_tree_function(file_name, text)
    inner('0', items)

def create_search_tree_function(file_name, text):
    with open('picarrow.item_id/functions/search_tree/{}.mcfunction'.format(file_name), 'w') as f:
        f.write(text)

def create_predicate(file_name, items):
    dct = {
        'condition': 'minecraft:entity_properties',
        'entity': 'this',
        'predicate': {
            'equipment': {
                'mainhand': {
                    'items': items
                }
            }
        }
    }
    path = 'picarrow.item_id/predicates/{}.json'.format(file_name)
    with open(path, 'w') as f:
        f.write(json.dumps(dct, indent=2) + '\n')

def read_items():
    items = []
    with open('items.txt') as f:
        for line in f:
            item = line.strip()
            items.append(item)
    return items

def read_tags(items):
    tags = {}
    for item in items:
        tags[item] = []
    for file in os.listdir('tags'):
        extension_start = file.rfind('.')
        if extension_start == -1:
            extension_start = len(file)
        tag = file[:extension_start]
        path = os.path.join('tags', file)
        with open(path) as f:
            for line in f:
                item = line.strip()
                tags[item].append(tag)
    return tags

if __name__ == '__main__':
    items = read_items()
    tags = read_tags(items)
    generate_namespace(tags)
