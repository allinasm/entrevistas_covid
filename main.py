import pandas as pd
from utils import count_occurrences
from utils import join_df
from utils import plot_partys
from utils import merge_df
from utils import grade_info
from utils import score_peop
from utils import economy_info
from utils import infected_info

path = 'data/covid_approval_polls.csv'
path2 = 'data/covid_concern_polls.csv'
path3 = 'data/pollster_ratings.xlsx'

# EXERCICI 1
print('===========EXERCICI 1===========')
count_occurrences(path)
print('1.2 Si el llegiria igual, perquè es llegeix linia a linia,'
      'és a dir, el temps dexecució és com a màxim n.')
print('1.3 Per aquest cas si hauria dimplementar una solució diferent,'
      'segurament fent un merge per unir els arxius i quedar-nos amb les\n'
      'dades que ens interesin per buscar els patrons')

# EXERCICI 2
print('===========EXERCICI 2===========')
approval_polls = join_df(path, path3)
concern_polls = join_df(path2, path3)
ratings_red = pd.read_excel(path3, engine='openpyxl', sheet_name=0,
                            usecols=["Pollster", "Banned by 538",
                                     "Predictive    Plus-Minus", "538 Grade"])
print('Dataframe approval_pols amb', len(approval_polls), ' files *', len(approval_polls.columns), 'columnes creat.')
print('Dataframe concern_pols amb', len(concern_polls), ' files *', len(concern_polls.columns), 'columnes creat.')
print('Dataframe ratings_red amb', len(ratings_red), ' files *', len(ratings_red.columns), 'columnes creat.')
# EXERCICI 3
print('===========EXERCICI 3===========')
plot_partys(approval_polls)

# EXERCICI 4
print('===========EXERCICI 4===========')
grade_df = merge_df(concern_polls, ratings_red)
economy_info(grade_df, plot_show=True)
infected_info(grade_df, plot_show=True)
grade_info(grade_df, plot_show=True)

# EXERCICI 5
print('===========EXERCICI 5===========')
print('Nombre de persones segons nivell de preocupació i data crítica')
score_peop(grade_df, 1.5, '2020-09-01', show_plot=True)
print('% de persones segons nivell de preocupació i data crítica')
score_peop(grade_df, 1.5, '2020-09-01', perc=True, show_plot=True)
print('5.2 Les gràfiques mostren uns patrons similars, estant la majoria de entrevistats molt preocupats.\n'
      'En percentatge abans de la data critica hi havia més gent molt preocupada que després ')
