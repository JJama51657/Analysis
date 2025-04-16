import pandas as pd
import matplotlib.pyplot as pt
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.0f}'.format)
# Read and clean up CSV
# Removes NA values
Ytlist = pd.read_csv(r"C:\Users\jjama\Downloads\Youtuber.csv").dropna()
Ytlist.drop(columns="Content Type", inplace=True)


def stuff(value):
    if "K" in value:
        return float(value.replace("K", "")) * 1000
    elif "M" in value:
        return float(value.replace("M", "")) * 1000000
    else:
        return float(value)


# This can be to figure out which yt channels have the biggest percentages between comments and their likes. to show user engagement
Ytlist["Average Views"] = Ytlist["Average Views"].apply(stuff)
Ytlist["Average Likes"] = Ytlist["Average Likes"].apply(stuff)
Ytlist["Average Comments"] = Ytlist["Average Comments"].apply(stuff)
Ytlist["Subscribers"] = Ytlist["Subscribers"].apply(stuff)

# Convert Data into numeric values, so that they can be analysed
################################ Table for Customer Enagement per influencer ####################
CSE_table = Ytlist.copy()
CSE_table["Engagement Activity"] = ((
    CSE_table["Average Likes"] + CSE_table["Average Comments"]) / CSE_table["Average Views"]) * 100
CSE_table.sort_values("Engagement Activity", ascending=False, inplace=True)
Final_CSET = CSE_table[["Channel Name",
                        "Engagement Activity", "Category"]][:30]  # Top 30 most customer engaging influencers
Final_CSET.drop(Final_CSET.index)
# Table for customer engagement completed.
#################################### Table for common categories ################################

Cat_tables = Final_CSET.copy()
Cat_tables["Engagement Activity"] = pd.to_numeric(
    Cat_tables["Engagement Activity"])
Final_Cat_table = Cat_tables[["Category", "Engagement Activity"]].groupby("Category").agg(
    {"Engagement Activity": pd.Series.sum})
Final_Cat_table.reset_index(inplace=True)
# Checking to see if categories are summed correctly

# Table For Most Common Categories Completed.
# print(Final_Cat_table, Final_CSET)


#################################### Table for Interactions per country #############################
Ct_Inters = Ytlist.copy()
Ct_Inters["Total Interactions"] = ((
    Ct_Inters["Average Likes"] + Ct_Inters["Average Comments"]) / Ct_Inters["Average Views"]) * 100
rct = Ct_Inters[["Country", "Total Interactions"]].groupby(
    "Country").agg({"Total Interactions": pd.Series.sum})
rct.sort_values("Total Interactions", inplace=True, ascending=False)
rct.reset_index(inplace=True)
print(rct)
#####################################################################################################
fig, ax = pt.subplots(figsize=(14, 9))  # Set figure size here

ax.bar(rct["Country"], rct["Total Interactions"])
ax.set_title("Engagement Per Country")
ax.set_ylabel("Total Engagement Activity")
ax.tick_params(axis='x', rotation=-30)

# Hide the 1e9 offset
ax.get_yaxis().get_offset_text().set_visible(False)

pt.tight_layout()
pt.show()
