

def count_occurrences(path):
    """ Produeix un recompte de quantes vegades
    apareix el patró Huffington Post i quantes
    url condueixen a un document pdf.

    Keyword arguments:
    path -- ruta de l'arxiu que conté els patrons a analitzar.
    """

    import re
    # declarem els comptadors
    huff_count = 0
    pdf_count = 0
    # llegim l'arxiu linia a linia i augmentem els comptadors si trobem el patró.
    with open(path, "r") as infile:
        for line in infile:
            if re.search(r"Huffington post\b", line, flags=re.IGNORECASE):
                huff_count += 1
            if re.search(r"https?:.*\.pdf/*$", line, flags=re.MULTILINE):
                pdf_count += 1

    print('El patró Huffington_post apareix %s vegades' % huff_count)
    print('El patró url_pdf apareix %s vegades' % pdf_count)
    return huff_count, pdf_count


def join_df(path1, path2):
    """ Produeix un dataframe amb les dades que ens interesen per
     resoldre els següents exercicis.

    Keyword arguments:
    path1 -- ruta de l'arxiu csv amb les entrevistes.
    path2 -- ruta de l'arxiu xlsx amb els agents entrevistadors.
    """

    import pandas as pd
    # Llegim els path generant dos dataframes
    df1 = pd.read_csv(path1)
    df2 = pd.read_excel(path2, engine='openpyxl')
    # Guardem les entrevistes sense 'tracking' amb agents entrevistadors
    # sense bannejar i que es trobin al llistat de l'excel.
    ndf1 = df1[df1["tracking"] == 0]
    ndf2 = df2[df2["Banned by 538"] == 'no']
    df = ndf1[ndf1["pollster"].isin(set(ndf2["Pollster"]))]
    return df


def plot_partys(df):
    """ Produeix un gràfic amb les persones que aproven i desaproven
    per les preguntes que contenen 'Trump' i 'coronavirus'. Dades agrupades
    per l'afinació a partits politics

    Keyword arguments:
    df -- dataframe que conté les dades a analitzar.
    """

    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    # Calculem el num de persones que aproven o desaproven (està registrat com a %.
    df['n_approve'] = (df['approve'] / 100) * (df['sample_size'])
    df['n_disapprove'] = (df['disapprove'] / 100) * (df['sample_size'])
    # Filtrem les entrevistes per les paraules esmentades i agrupem les dades
    df = df[df['text'].str.contains("Trump" and "coronavirus")]
    plot_df = df.groupby('party').sum()
    # imprimim i plotejem els resultats
    print(plot_df[['n_approve', 'n_disapprove']])
    plot_df[['n_approve', 'n_disapprove']].plot.barh()
    plt.show()
    return len(plot_df.columns)


def merge_df(df1, df2):
    """ Genera un dataframe seleccionant les columnes que ens
    interessen dels dos dataframes, eliminant valors NA, i actualitza
    les notes de '538 Grade' simplificant-les.

    Keyword arguments:
    df1 -- dataframe que conté les dades de les entrevistes.
    df2 -- dataframe que conté les dades sobre els agents entrevistadors.
    """

    # Generem el dataframe
    df = df1[['pollster', 'sample_size', 'party', 'end_date',
              'subject', 'very', 'somewhat', 'not_very', 'not_at_all']].merge(
        df2[['Pollster', '538 Grade', 'Predictive    Plus-Minus']],
        left_on='pollster', right_on='Pollster', how='left').dropna()
    # Simplifiquem les notes
    df['538 Grade'] = df['538 Grade'].map({'A': 'A', 'B': 'B',
                                           'B-': 'B', 'B/C': 'C', 'C-': 'C', 'D-': 'D'})
    return df


def grade_info(df, plot_show=False):
    """ Genera un gràfic amb el nombre de persones entrevistades
    agrupades per la nota de l'entrevistador.

        Keyword arguments:
        df -- dataframe que conté les dades seleccionades de les entrevistes
        i els entrevistadors.
        plot_show -- mostra el gràfic generat, per defecte False.
        """

    import matplotlib.pyplot as plt
    # Generem el dataframe agrupat
    plot_df = df.groupby(['538 Grade'])['sample_size'].sum()
    # Produim el gràfic
    if plot_show:
        plot_df.plot.bar()
        plt.title('Nombre entrevistes per nota')
        plt.xlabel('Notes')
        plt.ylabel('número entrevistats')
        plt.show()
    print('Nombre de persones entrevistades per nota:', plot_df)
    return plot_df


def economy_info(df, plot_show=False):
    """ Dona informació sobre la preocupació de les persones
    entrevistades per l'economia (en nombre de persones).

    Keyword arguments:
    df -- dataframe que conté les dades seleccionades de les entrevistes
    i els entrevistadors.
    plot_show -- mostra el gràfic generat, per defecte False.
    """

    import matplotlib.pyplot as plt
    # Nombre de persones entrevistades
    people = df['sample_size'].sum()
    # dataframe de persones que nombren 'economy' a 'subject'
    economy = df[df['subject'].str.contains("economy")]
    # guardem en variables el nombre d'entrevistats amb el grau de preocupació a estudiar
    very = (economy['very'] / 100 * economy['sample_size']).sum()
    not_at_all = (economy['not_at_all'] / 100 * economy['sample_size']).sum()
    print('El nombre total de persones entrevistades és: %s' % people)
    print("El nombre d'entrevistats molt preocupats per l'economia és: %s" % very)
    print("El nombre d'entrevistats gens preocupats per l'economia és: %s" % not_at_all)
    # Plotegem resultats
    if plot_show:
        preocup = ['very', 'not_at_all']
        n_entrev = [very, not_at_all]

        plt.bar(preocup, n_entrev)
        plt.title('Preocupació per economia Vs nombre entrevistats')
        plt.xlabel('preocupació')
        plt.ylabel('número entrevistats')
        plt.show()
    return very, not_at_all


def infected_info(df, plot_show=False):
    """ Dona informació sobre la preocupació de les persones
    entrevistades per l'infecció (en % de persones).

    Keyword arguments:
    df -- dataframe que conté les dades seleccionades de les entrevistes
    i els entrevistadors.
    plot_show -- mostra el gràfic generat, per defecte False.
    """

    import matplotlib.pyplot as plt
    # dataframe de persones que nombren 'infected' a 'subject'
    infected = df[df['subject'].str.contains("infected")]
    # guardem en variables el nombre d'entrevistats amb el grau de preocupació a estudiar
    very_i = ((infected['very'] / 100 * infected['sample_size']).sum() / infected['sample_size'].sum()) * 100
    not_at_all_i = (infected['not_at_all'] / 100 * infected['sample_size']).sum() / infected['sample_size'].sum() * 100
    print("El % d'entrevistats molt preocupats per l'infecció és: {}".format(very_i))
    print("El % d'entrevistats gens preocupats per l'infecció és: {}".format(not_at_all_i))
    # plotegem resultats
    if plot_show:
        preocup = ['very', 'not_at_all']
        n_entrev = [very_i, not_at_all_i]

        plt.bar(preocup, n_entrev)
        plt.title('Preocupació per infecció Vs % entrevistats')
        plt.xlabel('preocupació')
        plt.ylabel('% entrevistats')
        plt.show()
    return very_i, not_at_all_i


def score_peop(df, score, date, perc=False, show_plot=False):
    """ Genera un df i un plot amb informació sobre el nombre de persones segons
    nivell de preocupació i segons si l'entrevista havia finalitzat abans de la
    data introduïda o després.

    Keyword arguments:
    df -- dataframe que conté les dades seleccionades de les entrevistes i els
    entrevistadors.
    score -- nombre enter igual o per sobre (>=) del qual és vol obtenir la informació
    date -- data en format string per la qual es vol fer el tall.
    perc -- mostra els resultats en %, per defecte False.
    plot_show -- mostra el gràfic generat, per defecte False.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    # Transformem les notes amb lletres en notes numèriques.
    df['Grade_num'] = df['538 Grade'].map({'A': 1, 'B': 0.5, 'C': 0, 'D': -0.5, 'F': -1})
    # Cream la columna 'score' que conté la puntuació sumant la nota i la columna 'Predictive Plus-Minus'
    df['score'] = df['Grade_num'] + df['Predictive    Plus-Minus']
    # Filtrem pel valor 'score'
    df = df[df['score'] >= score].copy()
    # Cream la columna 'tall' per introduïr si l'entrevista és va produïr abans o despŕes de la data límit.
    df['tall'] = np.where(df.end_date < date, 'Abans', 'Després')
    # Transformem les columnes referents a la preocupació en nombres absoluts (estan en %).
    for col in df[['very', 'somewhat', 'not_very', 'not_at_all']]:
        df[col] = round(df[col] / 100 * df['sample_size'], 0)
    # Generem el df agrupat
    people_df = df.groupby(['tall'])[['sample_size', 'very', 'somewhat', 'not_very', 'not_at_all']].sum()
    # Si la opció perc no està activada s'imprimeix el df
    if not perc:
        print(people_df)
        # si l'opció show_plot és activada, mostrem el plot
        if show_plot:
            people_df[['very', 'somewhat', 'not_very', 'not_at_all']].plot.barh()
            plt.title('Nivell de preocupació segons data crítica')
            plt.xlabel('Nombre persones')
            plt.show()
    # Si està activada generem els percentatges per tall
    else:
        people_df = people_df.copy()
        for group in ['very', 'somewhat', 'not_very', 'not_at_all']:
            people_df[group] = round(people_df[group] / people_df['sample_size'] * 100, 2)
        print(people_df)
        # si l'opció show_plot és activada, mostrem el plot
        if show_plot:
            people_df[['very', 'somewhat', 'not_very', 'not_at_all']].plot.barh()
            plt.title('% de preocupació per grup abans/després de data crítica')
            plt.xlabel('% de persones persones')
            plt.show()
    return len(df[df['tall'] == 'Abans']), len(df[df['tall'] == 'Després'])
