import altair as alt
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np


class Viz:
    def __init__(self):
        print('new instance of Viz class')

    def createSpider(self, df, x, y, ax, subs, final=False):
        # Libraries

        # number of variable
        temp = df.drop(["name"], axis=1)
        normalized_df = temp.rank(pct=True)
        categories = list(normalized_df)
        N = len(categories)

        subs = subs
        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:

        ax.set_title(str(df['name'].iloc[x * subs + y][:17]) + '...', fontsize=8)
        values = normalized_df.iloc[x * subs + y].values.flatten().tolist()
        values += values[:1]
        values

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        angles += angles[:1]

        # Draw one axe per variable + add labels
        if final:
            ax.set_title(df['name'].iloc[x * subs + y], fontsize=16)
            plt.xticks(angles[:-1], categories, color='Black', size=10)

        # Draw ylabels
        # ax.set_rlabel_position(0)
        # ax.set_ylim([0,1])

        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid')

        # Fill area
        ax.fill(angles, values, 'b', alpha=0.1)

        return plt


    def spiders(self, df, subs):
        # Initialise the spider plot
        temp = df.drop(["name"], axis=1)
        normalized_df = temp.rank(pct=True)
        categories = list(normalized_df)
        N = len(categories)

        fig, axes = plt.subplots(subs, subs, subplot_kw=dict(polar=True))
        fig.suptitle("Song Feature Plots")
        fig.set_size_inches(18.5, 10.5)
        x = y = 0

        for axisRow in axes:
            for ax in axisRow:
                ax.set_title(temp.iloc[x, y])
                ax.set_yticklabels([])
                ax.set_xticklabels([])
                ax.yaxis.grid(False)
                ax.spines['polar'].set_visible(False)
                self.createSpider(df, x, y, ax, subs)

                y += 1
                y = y % subs
            x += 1
            x %= subs

        plt.savefig('spiderPlots.png')
        plt.subplots_adjust(wspace=.4, hspace=.4)
        return plt

    def graphMeans(self, audioFeaturesDF):
        source = pd.DataFrame(audioFeaturesDF.drop(
            columns=['timeSignature', 'tempo', 'loudness']))


        source = pd.DataFrame(source.mean(axis=0), columns=['Mean']).reset_index()
        return alt.Chart(source).mark_bar().encode(x='index', y='Mean')


# audioFeaturesDF = pd.read_csv('./Data/mikeydays/country/SongFeatures.csv')
# viz = Viz()
# # print(viz.spiders(audioFeaturesDF[:64], 8).show())


# new_ax = plt.subplot(111, polar=True)
# new_ax.set_yticklabels([])
# print(viz.createSpider(audioFeaturesDF[:], 5, 0, new_ax, 8, True).show())
