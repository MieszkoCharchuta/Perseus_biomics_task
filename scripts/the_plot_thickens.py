import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
expected = pd.read_csv("../data/ZymoD6322_expected_profile.csv")
measured = pd.read_csv("../data/ZymoD6322_3296B_classification_rates.csv", skiprows = 1)

merged_data = pd.merge(expected, measured, on='species')
del expected
del measured
merged_data = merged_data[['species', 'genomic abundance expected', 'abundance [%]']]
merged_data.rename(columns={"abundance [%]": "measured"}, inplace=True)
merged_data.rename(columns={"genomic abundance expected": "expected"}, inplace=True)
merged_data['species'] = merged_data['species'].str.replace('_complete_genome', '')
merged_data['species'] = merged_data['species'].str.replace('_', ' ')
merged_data = merged_data.set_index("species")
x = ["expected", "measured"]
list_of_species = merged_data.index.to_list()

plt.figure(figsize = [20, 10])
fig, ax = plt.subplots()

bar = ax.bar(x = x, height = merged_data.loc[[list_of_species[0]]].to_numpy()[0], width = 0.2, align = "center")
ax.bar_label(bar,label_type='center')
bottom = merged_data.loc[[list_of_species[0]]].to_numpy()[0]

for i in range(1, len(merged_data.index.to_list())):
  bar = ax.bar(x = x, height = merged_data.loc[[list_of_species[i]]].to_numpy()[0], width = 0.2, bottom = bottom, align = "center")
  ax.bar_label(bar,label_type='center')
  bottom+=merged_data.loc[[list_of_species[i]]].to_numpy()[0]
  
ax.set_ylabel('Species abundance [% bp]')

ax.legend(labels = list_of_species)
plt.show()
plt.savefig("../figures/species_abundance.png", dpi='figure', format='png')

plt.clf()


# I will add the data for phyla manually, 
# since normally it would be part of my dataset already (as per industry standards)
# merged_data.to_csv("species_and_their_phyla.xlsx", index=True)

phyla_abundances = pd.read_csv("../data/species_and_their_phyla.csv")
phyla_abundances = phyla_abundances[['phylum', 'expected', 'measured']]
phyla_abundances = phyla_abundances.groupby("phylum").sum()
phyla_abundances = phyla_abundances.set_index("phylum")

x = ["expected", "measured"]
list_of_phyla = phyla_abundances.index.to_list()

plt.figure(figsize = [20, 10])
fig, ax = plt.subplots()

bar = ax.bar(x = x, height = phyla_abundances.loc[[list_of_phyla[0]]].to_numpy()[0], width = 0.2, align = "center")
ax.bar_label(bar,label_type='center')
bottom = phyla_abundances.loc[[list_of_phyla[0]]].to_numpy()[0]

for i in range(1, len(phyla_abundances.index.to_list())):
  bar = ax.bar(x = x, height = phyla_abundances.loc[[list_of_phyla[i]]].to_numpy()[0], width = 0.2, bottom = bottom, align = "center")
  ax.bar_label(bar,label_type='center')
  bottom+=phyla_abundances.loc[[list_of_phyla[i]]].to_numpy()[0]
  
ax.set_ylabel('Phyla abundance [% bp]')

ax.legend(labels = list_of_phyla)
plt.show()
plt.savefig("../figures/phyla_abundance.png", dpi='figure', format='png')

plt.clf()
