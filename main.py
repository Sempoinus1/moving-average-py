import pandas
import matplotlib.pyplot as plt
import numpy as np

# Výpočet klouzavého průměru


def moving_average(signal, period):
    buffer = [np.nan] * period
    for i in range(period, len(signal)):
        buffer.append(signal[i-period:i].mean())
    return buffer


def main():
    # Parsování csv souboru
    csv = pandas.read_csv('./pid.csv', index_col=None)
    ascend = csv['narust'].to_numpy()
    identify = csv['_id'].to_numpy()


    # uložení klouzavého průměru do numpy array
    avg = np.array(moving_average(ascend, 10))
    # zjištění protnutí průměru a nárůstového grafu
    idx = np.argwhere(np.diff(np.sign(ascend - avg))).flatten()
    # Zobrazení grafů
    plt.plot(identify, avg, label="Simple Moving Average")
    plt.plot(identify, ascend, label="Původní")
    plt.plot(identify[idx], avg[idx], 'ro', label="Protnuté body")


    # Příprava textu pro zapsání do tabulky
    collabel = ("Protnutí dnů ", "Protnutí nárůstů")
    celltext = np.array([identify[idx], avg[idx]])
    celltext = np.swapaxes(celltext, 0, 1)
    # Odstranění nan hodnot z pole
    celltext = celltext[~np.any(np.isnan(celltext), axis=1)]

    # Nastavení zobrazení tabulky a grafu
    table = plt.table(cellText=celltext, colLabels=collabel, loc="right")
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(0.6, 0.455)
    plt.subplots_adjust(right=0.65)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            ncol=2, mode="expand", borderaxespad=0.)
    plt.xlabel('Měřené dny')
    plt.ylabel('Nárůst')
    plt.show()

if __name__ == "__main__":
    main()