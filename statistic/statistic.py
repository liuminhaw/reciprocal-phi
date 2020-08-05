# -*- coding:UTF-8 -*-


# Standard library imports
import os, sys
import random
from datetime import datetime

# Local application imports
from general_pkg import env
from general_pkg import google_cred as cred

from module_pkg import logging_class as logcl
from module_pkg import conf_mod
from module_pkg import sheet


INT32_MAX = 2147483647

logger = logcl.PersonalLog('rpdi-statistic', env.LOG_DIR)


# --- CODING BLOCKS ---
# --- ------------- ---

def main():

    # TODO: argparse for version information

    # Check for config file existence
    try:
        config = conf_mod.Config(env.CONFIG_FILE)
    except FileNotFoundError as err:
        logger.warning('Config file {} not found: {}'.format(env.CONFIG_FILE, err))
        sys.exit(11)
    except conf_mod.configError as err:
        logger.warning('Wrong configuration: {}'.format(err))
        sys.exit(12)

    # Set date data
    current_datetime = datetime.now()
    format_datetime = current_datetime.strftime('%Y%m%d-%H%M%S')

    # Config info
    logger.info('Sheet: {}'.format(config.sheet))
    logger.info('Sheet id: {}'.format(config.sheet_id))

    logger.info('Ingredients: {}'.format(config.ingredients))
    logger.info('Sequence pick amount: {}'.format(config.pick))

    credential = cred.google_credential(config.sheet_cred)
    stat_sheet = sheet.StatsSheet(credential, config.sheet_id)

    # Prepare sheet
    new_sheetname = '{}_{}'.format(env.SHEETNAME_PREFIX, format_datetime)
    new_sheetid = random.randrange(INT32_MAX)
    stat_sheet.create_new_sheet(new_sheetname, sheet_id=int(new_sheetid))
    stat_sheet.statistic_write('A1', [['Raw', '', 'Refined', '']])
    stat_sheet.statistic_write('A2', [['sequence', 'count', 'sequence', 'count']])

    # Compute statistic
    statistic = _statistic()
        
    print('General statistic:')
    total = 0
    for key, value in statistic.items():
        print('key: {}, value: {}'.format(key, value))
        total += value
    print('Total: {}'.format(total))

    # TODO: Write to sheet 
    sheet_data = sheet.statistic_to_data(statistic) 
    print('Sheet data: {}'.format(sheet_data))
    stat_sheet.statistic_write('A3', sheet_data)

    statistic = _statistic_refine(statistic)
        
    print('Refined statistic:')
    total = 0
    for key, value in statistic.items():
        print('key: {}, value: {}'.format(key, value))
        total += value
    print('Total: {}'.format(total))

    # TODO: Write to sheet
    sheet_data = sheet.statistic_to_data(statistic) 
    print('Sheet data: {}'.format(sheet_data))
    stat_sheet.statistic_write('C3', sheet_data)


def _init_ingredients_list(config, ingredients_list):
    """
    Check for empty ingredients after ingredients list initialized
    """
    for key, value in config.ingredients.items():
        if value == 0:
            ingredients_list.remove(key)


def _statistic():
    """
    Picking ingredients in order and count occur time of each sequence
    """
    config = conf_mod.Config(env.CONFIG_FILE)
    ingredients = list(config.ingredients)
    _init_ingredients_list(config, ingredients)

    statistic = {}

    while ingredients:

        selected_seq = []
        for _ in range(config.pick):
            # Empty list, no ingredient left
            if not ingredients:
                logger.info('No enough ingredients: {}'.format(config.ingredients))
                break

            ingredient = random.choice(ingredients)
            config.ingredients[ingredient] -= 1
            selected_seq.append(ingredient)
            if config.ingredients[ingredient] == 0:
                ingredients.remove(ingredient)

        if len(selected_seq) != config.pick:
            continue

        selected_seq = tuple(selected_seq)
        if selected_seq in statistic:
            statistic[selected_seq] += 1
        else:
            statistic[selected_seq] = 1

    return statistic

def _statistic_refine(statistic):
    """
    Picking ingredients in order and count occur time of each sequence,
    sequence are view as same if sequence == reversed sequence
    """
    refined_statistic = {}

    for key, value in statistic.items():
        seq = list(key)
        reversed_seq = seq.copy()
        reversed_seq.reverse()

        seq = tuple(seq)
        reversed_seq = tuple(reversed_seq)
        if seq not in refined_statistic and reversed_seq not in refined_statistic:
            refined_statistic[seq] = statistic[seq]
        elif seq in refined_statistic:
            refined_statistic[seq] += statistic[seq]
        else:
            refined_statistic[reversed_seq] += statistic[seq]

    return refined_statistic




if __name__ == '__main__':
    main()