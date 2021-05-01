# ## MTG Standard Cards

# ### 'Gather' data from MTG JSON


#import packages
import pandas as pd
import requests as re
#load json from url
mtgjson = re.get('https://mtgjson.com/api/v5/Standard.json')
#check connection
print(mtgjson.status_code)


# ### 'Draw' cards by set


#convert to dict
mtgjson_d = mtgjson.json()
#convert from dict to df
sets = pd.DataFrame(mtgjson_d)
#clean to exclude metadata - should only be one field 'data' containing all card information for each set
sets = sets.iloc[2:,[1]].copy()
#
#extract data for each set
#the structure of the json dicts is: {'data' : {'set' : {'cards': {x}}}}
#want cards, list of dicts
#Ex. eld = sets['data'][0]['cards']
#
def cards_data(dict):
    return dict['cards']
#organize all cards data as list of dicts in a table indexed by set
sets['cards'] = sets.apply(lambda x : cards_data(x['data']), axis= 1)
sets = sets[['cards']].copy()


# ### 'Summon' attributes for each card and combine all cards in tabular form


#extract card attributes for each card in the set
#combine them later in tabular form
def list_by_set(list_of_dicts, key_name):
    target_list = []
    for d in list_of_dicts:
        if key_name in d.keys():
            target_list.append(d[key_name])
        else:
        #fill in missing information with blanks (keep same number of records)
            target_list.append('')
    return target_list
#
standard_cards = pd.DataFrame()
#
for i in range(len(sets['cards'])):
    current_set = sets.index[i]
    all_attributes_set = sets['cards'][i]
    #extract list of attributes for all cards in set
    i_names = list_by_set(all_attributes_set, 'name')
    i_colors = list_by_set(all_attributes_set, 'colors')
    i_colorid = list_by_set(all_attributes_set, 'colorIdentity')
    i_type = list_by_set(all_attributes_set, 'types')
    i_subtype = list_by_set(all_attributes_set, 'subtypes')
    i_text = list_by_set(all_attributes_set, 'text')
    i_power = list_by_set(all_attributes_set, 'power')
    i_toughness = list_by_set(all_attributes_set, 'toughness')
    i_cmc = list_by_set(all_attributes_set, 'convertedManaCost')
    i_rarity = list_by_set(all_attributes_set, 'rarity')
    i_printings = list_by_set(all_attributes_set, 'printings')
    i_keywords = list_by_set(all_attributes_set, 'keywords')
    i_layout = list_by_set(all_attributes_set, 'layout')
    i_side = list_by_set(all_attributes_set, 'side')
    #
    #set up pandas DataFrame
    #combine all lists of attributes into list (of lists)
    list_of_attributes = [i_names, i_colors, i_colorid, i_type, i_subtype, i_text, i_power, i_toughness, i_cmc, i_rarity, i_printings, i_keywords, i_layout, i_side]  
    #zip attributes with field names before converting to DataFrame
    dict_for_df = dict(zip(['Name', 'Color', 'ColorID', 'Type', 'Subtype', 'Text', 'Power', 'Toughness', 'CMC', 'Rarity', 'Printings', 'Keywords', 'Layout', 'Side'], list_of_attributes))
    #convert dict to DataFrame
    set_cards = pd.DataFrame(dict_for_df)
    set_cards['Set'] = current_set = sets.index[i]
    #
    standard_cards = standard_cards.append(set_cards)
    #
standard_cards = standard_cards.reset_index().drop(columns= 'index')


# ### Prettify table and output as .csv file

standard_cards['Name'] = standard_cards['Name'].astype('str')
standard_cards['Type'] = standard_cards['Type'].astype('str').str.strip("[]").str.replace("'", "")
standard_cards['Subtype'] = standard_cards['Subtype'].astype('str').str.strip("[]").str.replace("'", "")
standard_cards['Color'] = standard_cards['Color'].astype('str').str.strip("[]").str.replace("'", "")
standard_cards['ColorID'] = standard_cards['ColorID'].astype('str').str.strip("[]").str.replace("'", "")
standard_cards['CMC'] = standard_cards['CMC'].astype('int64')
standard_cards['Rarity'] = standard_cards['Rarity'].astype('str').str.capitalize()
standard_cards['Printings'] = standard_cards['Printings'].astype('str').str.strip("[]").str.replace("'", "")
standard_cards['Keywords'] = standard_cards['Keywords'].astype('str').str.strip("[]").str.replace("'", "")
standard_cards['Layout'] = standard_cards['Layout'].astype('str').str.capitalize()
#
standard_cards = standard_cards[['Name', 'Set', 'Color', 'ColorID', 'Type', 'Subtype', 'CMC', 'Rarity', 'Text', 'Keywords', 'Power', 'Toughness', 'Printings', 'Layout', 'Side']]
standard_cards.to_csv('mtg_standard_cards.csv', index= False)
