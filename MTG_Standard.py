#Extract data
#import packages
import pandas as pd
import requests as re
#load from url
mtgjson = re.get('https://mtgjson.com/json/Standard.json')
mtgjson.status_code
#convert to dict
mtgjson_d = mtgjson.json()
type(mtgjson_d)
#convert from dict to df
sets = pd.DataFrame(mtgjson_d).transpose()
#Set up Cards dataframe
#Step 1: create function to get all attributes by key in cards dict
def get_cardstuff(list_of_dicts, key):
    a_list = []
    for d in list_of_dicts:
        if key in d.keys():
            a_list.append(d.get(key))
        else:
            a_list.append('')
    return a_list
#this works for pulling out data by key in dict
#Step 2: apply function to 'sets' df
sets['Name'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'name'), axis= 1)
sets['Color'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'colors'), axis= 1)
sets['ColorID'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'colorIdentity'), axis= 1)
sets['Type'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'types'), axis= 1)
sets['Subtype'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'subtypes'), axis= 1)
sets['Text'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'text'), axis= 1)
sets['Power'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'power'), axis= 1)
sets['Toughness'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'toughness'), axis= 1)
sets['CMC'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'convertedManaCost'), axis= 1)
sets['Rarity'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'rarity'), axis= 1)
sets['Printings'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'printings'), axis= 1)
sets['Prices'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'prices'), axis= 1)
sets['Layout'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'layout'), axis= 1)
sets['Side'] = sets.apply(lambda x: get_cardstuff(x['cards'], 'side'), axis= 1)
#rename old 'name' column to 'Set' to avoid confusion
sets['Set'] = sets['name']
#Now have additional columns; each contains a list of interesting attributes for all cards in Standard
#Step 3: make new function to pull out each item from the series of lists made previously.
def get_list_item(series_of_lists):
    a_list = []
    for l in series_of_lists:
        for i in l:
            a_list.append(i)
    return a_list
#use this function to create new, expanded df with ALL the cards in ALL Standard sets
#Step 4: expand the index and set names of sets df
set_list = []
setid_list = []
for i in sets.index:
    set_name = sets.loc[i, 'name']
    set_id = i
    for j in sets.loc[i, 'cards']:
        set_list.append(set_name)
        setid_list.append(set_id)
#use as set ID in new df: cards table
#Step 5: apply 'get_list_item' to blow up list
name_list = get_list_item(sets['Name'])
color_list = get_list_item(sets['Color'])
colorID_list = get_list_item(sets['ColorID'])
type_list = get_list_item(sets['Type'])
subtype_list = get_list_item(sets['Subtype'])
text_list = get_list_item(sets['Text'])
power_list = get_list_item(sets['Power'])
toughness_list = get_list_item(sets['Toughness'])
cmc_list = get_list_item(sets['CMC'])
rarity_list = get_list_item(sets['Rarity'])
printings_list = get_list_item(sets['Printings'])
prices_list = get_list_item(sets['Prices'])
layout_list = get_list_item(sets['Layout'])
side_list = get_list_item(sets['Side'])
#use each list as series for new df: cards table
#Step 6: create the cards table from dict
new_list_of_lists = [set_list, setid_list, name_list, color_list, colorID_list, type_list, subtype_list, text_list, power_list, toughness_list, cmc_list, rarity_list,
                     printings_list, prices_list, layout_list, side_list]
new_dict = dict(zip(['Set', 'SetID', 'Name', 'Color', 'ColorID', 'Type', 'Subtype', 'Text', 'Power', 'Toughness', 'CMC', 'Rarity', 'Printings', 'Prices', 'Layout', 'Side'], 
                    new_list_of_lists))
cards = pd.DataFrame(new_dict)
#Step 7: format dtypes and clean up strings to make it more readable
cards['Name'] = cards['Name'].astype('str')
cards['Type'] = cards['Type'].astype('str').str.strip("[]").str.replace("'", "")
cards['Subtype'] = cards['Subtype'].astype('str').str.strip("[]").str.replace("'", "")
cards['Color'] = cards['Color'].astype('str').str.strip("[]").str.replace("'", "")
cards['ColorID'] = cards['ColorID'].astype('str').str.strip("[]").str.replace("'", "")
cards['SetID'] = cards['SetID'].astype('str')
cards['Set'] = cards['Set'].astype('str')
cards['CMC'] = cards['CMC'].astype('int64')
cards['Rarity'] = cards['Rarity'].astype('str').str.capitalize()
cards['Printings'] = cards['Printings'].astype('str').str.strip("[]").str.replace("'", "")
#Step 8: find and remove dups
dups = cards[cards.duplicated(subset= 'Name')]
#dups occur where name & set is the same, otherwise it's just a reprint
#remove all dups of name AND set in sets_df
cards = cards.drop_duplicates(subset = ['Name', 'SetID'])
#Note: this also gets rid of the different basic land versions, but going to remove lands anyway
cards.to_csv(path_or_buf='mtg_standard.csv', index= False)