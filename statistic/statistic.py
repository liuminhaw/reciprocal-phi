# -*- coding:UTF-8 -*-


# Standard library imports
import os, sys
import random

# Local application imports
from general_pkg import env

from module_pkg import logging_class as logcl
from module_pkg import conf_mod

logger = logcl.PersonalLog('rpdi-statistic', env.LOG_DIR)


# --- CODING BLOCKS ---
# --- ------------- ---

def main():

    # Check for config file existence
    try:
        config = conf_mod.Config(env.CONFIG_FILE)
    except FileNotFoundError as err:
        logger.warning('Config file {} not found: {}'.format(env.CONFIG_FILE, err))
        sys.exit(11)
    except conf_mod.configError as err:
        logger.warning('Wrong configuration: {}'.format(err))
        sys.exit(12)

    print(config.ingredients)
    print(config.pick)

    ingredients_list = list(config.ingredients)
    print(ingredients_list)

    # Check for empty ingredients
    rm_keys = []
    for key, value in config.ingredients.items():
        if value == 0:
            rm_keys.append(key)
            ingredients_list.remove(key)


    statistic = {}
    while ingredients_list:
        selected_seq = []
        for _dummy in range(config.pick):
            if not ingredients_list:
                logger.info('No enough ingredients: {}'.format(config.ingredients))
                break

            ingredient = random.choice(ingredients_list)
            config.ingredients[ingredient] -= 1
            selected_seq.append(ingredient)
            if config.ingredients[ingredient] == 0:
                ingredients_list.remove(ingredient)

        if len(selected_seq) != config.pick:
            continue

        selected_seq = tuple(selected_seq)
        if selected_seq in statistic:
            statistic[selected_seq] += 1
        else:
            statistic[selected_seq] = 1
        
    total = 0
    for key, value in statistic.items():
        print('key: {}, value: {}'.format(key, value))
        total += value

    print('Total: {}'.format(total))






if __name__ == '__main__':
    main()