import unittest
import pandas as pd
from utils import count_occurrences
from utils import join_df
from utils import plot_partys
from utils import merge_df
from utils import grade_info
from utils import score_peop
from utils import economy_info
from utils import infected_info


class TestScenarios(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("Carregant paths i dfs d'entrada")
        self.path = 'data/covid_approval_polls.csv'
        self.path2 = 'data/covid_concern_polls.csv'
        self.path3 = 'data/pollster_ratings.xlsx'
        self.ratings_df = pd.read_excel(self.path3, engine='openpyxl', sheet_name=0, usecols=[
            "Pollster", "Banned by 538", "Predictive    Plus-Minus", "538 Grade"])
        print("Càrrega completa")

    def test_ocurrence(self):
        print('Començant test_ocurrence')
        self.assertEqual(count_occurrences(self.path), (112, 1332))
        print('test_ocurrence finalitzat')

    def test_join(self):
        print("Començant test_join")
        self.df = join_df(self.path, self.path3)
        self.df2 = join_df(self.path2, self.path3)
        self.assertEqual((len(self.df), len(self.df.columns)), (1133, 13))
        self.assertEqual((len(self.df2), len(self.df2.columns)), (246, 15))
        print('test_join finalitzat')

    def test_partys(self):
        print('començant test_partys')
        df = join_df(self.path, self.path3)
        self.assertEqual(plot_partys(df), 5)
        print('test_partys finalitzat')

    def test_merge(self):
        print('començant test_merge')
        df1 = join_df(self.path2, self.path3)
        df = merge_df(df1, self.ratings_df)
        self.assertEqual(df['538 Grade'].nunique(), 4)
        print('test_merge finalitzat')

    def test_grade_info(self):
        print('començant test_grade_info')
        df1 = join_df(self.path2, self.path3)
        df = grade_info(merge_df(df1, self.ratings_df), plot_show=True)
        self.assertEqual(len(df), 4)
        print('test_grade_info finalitzat')

    def test_economy(self):
        print('començant test_economy')
        df1 = join_df(self.path2, self.path3)
        df = merge_df(df1, self.ratings_df)
        self.assertEqual(economy_info(df, plot_show=True), (654472.84, 28491.6))
        print('test_economy finalitzat')

    def test_infected(self):
        print('començant test_infected')
        df1 = join_df(self.path2, self.path3)
        df = merge_df(df1, self.ratings_df)
        self.assertEqual(infected_info(df, plot_show=True), (22.34405107218159, 12.574884035143235))
        print('test_infected finalitzat')

    def test_score(self):
        print('Començant test_score')
        df1 = join_df(self.path2, self.path3)
        df = merge_df(df1, self.ratings_df)
        self.assertEqual(score_peop(df, 1.5, '2020-09-01', show_plot=True), (15, 9))
        self.assertEqual(score_peop(df, 1.5, '2020-09-01', perc=True, show_plot=True), (15, 9))
        print('test_score finalitzat')
