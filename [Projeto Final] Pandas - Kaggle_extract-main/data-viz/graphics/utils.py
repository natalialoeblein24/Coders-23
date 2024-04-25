import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


def two_feature_classification(df, target, f1, f2):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.set_facecolor("#393838")

    X = df.drop(target, axis=1)
    y = df[target].values

    labels = df[target].value_counts().index.tolist()

    ax.scatter(
        X.loc[y == 0, f1],
        X.loc[y == 0, f2],
        label=labels[0],
        alpha=1,
        linewidth=0,
        c="#0EB8F1",
    )
    ax.scatter(
        X.loc[y == 1, f1],
        X.loc[y == 1, f2],
        label=labels[1],
        alpha=1,
        linewidth=0,
        c="#F1480F",
        marker="X",
    )

    ax.set_title("Distribution of " + target + " w.r.t " + f1 + " and " + f2)
    ax.set_xlabel(f1)
    ax.set_ylabel(f2)
    ax.legend()
    sns.despine(top=True, right=True, left=True, bottom=True)
    plt.show()


def feature_distribution(df, col):
    skewness = np.round(df[col].skew(), 3)
    kurtosis = np.round(df[col].kurtosis(), 3)

    fig, axes = plt.subplots(1, 3, figsize=(21, 7))

    sns.kdeplot(data=df, x=col, fill=True, ax=axes[0], color="#603F83", linewidth=2)
    sns.boxplot(
        data=df,
        y=col,
        ax=axes[1],
        color="#603F83",
        linewidth=2,
        flierprops=dict(marker="x", markersize=3.5),
    )
    stats.probplot(df[col], plot=axes[2])

    axes[0].set_title(
        "Distribution \nSkewness: " + str(skewness) + "\nKurtosis: " + str(kurtosis)
    )
    axes[1].set_title("Boxplot")
    axes[2].set_title("Probability Plot")
    fig.suptitle("For Feature:  " + col)

    for ax in axes:
        ax.set_facecolor("#C7D3D4FF")
        ax.grid(linewidth=0.1)

    axes[2].get_lines()[0].set_markerfacecolor("#8157AE")
    axes[2].get_lines()[0].set_markeredgecolor("#603F83")
    axes[2].get_lines()[0].set_markeredgewidth(0.1)
    axes[2].get_lines()[1].set_color("#F1480F")
    axes[2].get_lines()[1].set_linewidth(3)

    sns.despine(top=True, right=True, left=True, bottom=True)
    plt.show()


def count_percentage(df, col, hue):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 6))
    order = sorted(df[col].unique())
    palette = ["#0EB8F1", "#F1480F", "#971194", "#FEE715", "#101820"]

    sns.countplot(
        col, data=df, hue=hue, ax=ax1, order=order, palette=palette[: df[hue].nunique()]
    )
    ax1.set_title("Counts For Feature:\n" + col)

    df_temp = (
        df.groupby(col)[hue]
        .value_counts(normalize=True)
        .rename("percentage")
        .reset_index()
    )

    fig = sns.barplot(
        x=col,
        y="percentage",
        hue=hue,
        data=df_temp,
        ax=ax2,
        order=order,
        palette=palette[: df[hue].nunique()],
    )
    fig.set_ylim(0, 1)

    fontsize = 14 if len(order) <= 10 else 8
    for p in fig.patches:
        txt = "{:.1f}".format(p.get_height() * 100) + "%"
        txt_x = p.get_x()
        txt_y = p.get_height()
        fig.text(txt_x + 0.125, txt_y + 0.02, txt, fontsize=fontsize)

    ax2.set_title("Percentages For Feature: \n" + col)
    plt.setp(ax1.get_xticklabels(), rotation=70, horizontalalignment="right")
    plt.setp(ax2.get_xticklabels(), rotation=70, horizontalalignment="right")

    for ax in [ax1, ax2]:
        ax.set_facecolor("#C7D3D4FF")
        ax.grid(linewidth=0.1)


def feature_dist_clas(df, col, hue):
    fig, axes = plt.subplots(1, 4, figsize=(25, 5))
    order = sorted(df[hue].unique())
    palette = ["#0EB8F1", "#F1480F", "#971194", "#FEE715", "#101820"]

    sns.histplot(
        x=col,
        hue=hue,
        data=df,
        ax=axes[0],
        palette=palette[: df[hue].nunique()],
        edgecolor="black",
        linewidth=0.5,
    )
    sns.kdeplot(
        x=col,
        hue=hue,
        data=df,
        fill=True,
        ax=axes[1],
        palette=palette[: df[hue].nunique()],
        linewidth=2,
    )
    sns.boxplot(
        y=col,
        hue=hue,
        data=df,
        x=[""] * len(df),
        ax=axes[2],
        palette=palette[: len(order)],
        linewidth=2,
        flierprops=dict(marker="x", markersize=3.5),
    )

    sns.violinplot(
        y=col,
        hue=hue,
        data=df,
        x=[""] * len(df),
        ax=axes[3],
        palette=palette[: df[hue].nunique()],
    )

    fig.suptitle("For Feature:  " + col)
    axes[0].set_title("Histogram For Feature " + col)
    axes[1].set_title("KDE Plot For Feature " + col)
    axes[2].set_title("Boxplot For Feature " + col)
    axes[3].set_title("Violinplot For Feature " + col)

    for ax in axes:
        ax.set_facecolor("#C7D3D4FF")
        ax.grid(linewidth=0.1)


def bar_box(df, col, target):
    fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharex=True)

    order = sorted(df[col].unique())
    palette = [
        "#0EB8F1",
        "#F1480F",
        "#971194",
        "#FEE715",
        "#101820",
        "#008B97",
        "#F1480F",
        "#9D9301",
        "#4C00FF",
        "#FF007B",
        "#00EAFF",
        "#9736FF",
        "#FFEE00",
        "#8992F3",
        "#282828",
        "#FFEF63",
        "#80004C",
        "#CFF839",
    ]

    sns.countplot(
        data=df, x=col, ax=axes[0], order=order, palette=palette[: len(order)]
    )
    sns.boxplot(
        data=df,
        x=col,
        ax=axes[1],
        y=target,
        order=order,
        palette=palette[: len(order)],
        flierprops=dict(marker="x", markersize=3.5),
    )

    fig.suptitle("For Feature:  " + col)
    axes[0].set_title("Countplot For " + col)
    axes[1].set_title(col + " --- " + target)

    for ax in axes:
        ax.set_facecolor("#C7D3D4FF")
        ax.grid(linewidth=0.1)
        plt.sca(ax)
        plt.xticks(rotation=90)


def plot_scatter(df, col, target):
    corr = df[[col, target]].corr()[col][1]
    c = (
        ["#EB0000"]
        if corr >= 0.7
        else (
            ["#800000"]
            if corr >= 0.3
            else (
                ["#FF6363"]
                if corr >= 0
                else (
                    ["#000EAA"]
                    if corr <= -0.7
                    else (["#3845D3"] if corr <= -0.3 else ["#6CAAFA"])
                )
            )
        )
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("#C7D3D4FF")
    ax.grid(linewidth=0.1)

    sns.scatterplot(x=col, y=target, data=df, c=c, ax=ax, edgecolor="black")
    ax.set_title(
        "Correlation between " + col + " and " + target + " is: " + str(corr.round(4))
    )


def heatmap(df):
    fig, ax = plt.subplots(figsize=(15, 15))

    sns.heatmap(
        df.corr(),
        cmap="coolwarm",
        annot=True,
        fmt=".2f",
        annot_kws={"fontsize": 9},
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.01,
        linecolor="black",
        cbar=False,
    )

    sns.despine(top=True, right=True, left=True, bottom=True)


def plot_correlation(df, method="pearson"):
    """
    df is the data frame with numerical or ordinal values.
    method is the correlation method used as described above.
    method takes values - {‘pearson’, ‘kendall’, ‘spearman’}
    default value is 'pearson'
    """
    sns.heatmap(
        df.corr(method=method),
        annot=True,
        fmt=".2f",
        cmap=sns.color_palette("magma"),
        linewidth=2,
        edgecolor="k",
        vmax=1.0,
        square=True,
    )
    plt.title("CORRELATION PLOT", fontsize=15)
    plt.show()
