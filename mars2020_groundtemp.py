#!/usr/bin/env python3
#
# Mars 2020 Perseverance Rover MEDA TIRS ground temperature data plotter
# Holger Isenberg areo.info 2026-04-21
#
# usage example: mars2020_groundtemp.py WE__0358___________CAL_TIRS________________P02.csv
#
# MEDA TIRS infrared probes:
# https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/PERSEVERANCE/meda.html
# https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2022JE007559
#
# ground temperature data:
# data from https://pds-atmospheres.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_calibrated_env/
#
# https://ui.adsabs.harvard.edu/abs/2016DPS....4812307P/abstract
# downward pointing thermopiles: IR3 (0.3-3 µm), IR4 (6.5-inf µm), IR5 (8-14 µm)
#
# https://pds-atmospheres.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/document/meda_release_notes.txt
# Update of thermopile responsivity degradation values (all channels:
# IR1, IR2, IR3, IR4 and IR5). Results obtained from the analysis of
# the new in-flight calibrations, as well as from the use of a linear
# interpolation of the degradation value between sols (degradation
# values obtained from in-flight calibrations carried out on specific
# campaigns and sols).
#
# At the moment, wind data beyond sol 315 is not provided due to
# certain damage to some components of the wind sensor, as a result of
# harsh weather conditions. Recalibration to compensate for the missing
# elements is ongoing.

import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv(sys.argv[1])

solstr = df['LMST'][1][:5]
sol = int(solstr)

df['LMST'] = df['LMST'].astype(str).str.slice(-12)
df['LMST'] = pd.to_timedelta(df['LMST']) / pd.Timedelta(hours=1)
df['GROUND_TEMP'] = df['GROUND_TEMP'].astype(float) - 273.15
df_good = df[(df['ROVER_STILL'] == 1) & 
             (df['TIRS_GROUND_FOOTPRINT_NOT_IN_SHADOW'] == 1) & 
             (df['GROUND_TEMP_UNCERTAINTY'] < 2)]

plt.figure(figsize=(10,8))
plt.scatter(df_good['LMST'], df_good['GROUND_TEMP'], s=5, label='Ground Temp °C')

ax = plt.gca()
ax.set_xlim([0, 24])
ax.set_ylim([-100, 40])
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.tick_params(axis='both', which='major')
plt.axhline(y=0, color='black')

plt.xlabel('Local Mean Solar Time Hours')
plt.ylabel('Ground Temperature °C')
plt.title('Mars 2020 Perseverance Rover MEDA TIRS: Ground Temperature on Sol ' + str(sol))
plt.annotate('Graph: mars2020_groundtemp.py at github.com/isenberg/areodata '
    + datetime.date.today().isoformat()
    + '\nData: NASA/JPL-Caltech / Centro de Astrobiología of Spain'
    + '\npds-atmospheres.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_calibrated_env',
    xy=(1, 0), xycoords='axes fraction',
    xytext=(-5, -40), textcoords='offset points',
    ha='right', va='top', fontsize=9)
plt.tight_layout()
plt.grid(True)
plt.legend()
plt.savefig('mars2020_groundtemp_sol' + solstr + '.png')
plt.show()
