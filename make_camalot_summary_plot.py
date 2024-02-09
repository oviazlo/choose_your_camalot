import matplotlib.pyplot as plt
from typing import NamedTuple
import seaborn as sns

class Camalot(NamedTuple):
    brand: str
    size: str
    min: float
    max: float
    weight: int

size_dict = {
    # https://blackdiamond-web.cdn.prismic.io/blackdiamond-web/f1e78696-cfb3-4824-9bff-a0ba977ef4ee_M13747_C_Camalot_C4-ULC4_IS-WEB.pdf
    "BD C4": {
        "0.3": (14.8, 21.0),
        "0.4": (16.6, 23.8),
        "0.5": (20.7, 29.8),
        "0.75": (25.2, 36.2),
        "1": (32.3, 45.7),
        "2": (40.6, 57.2),
        "3": (54.4, 77.5),
        "4": (70.9, 102.4)
    },
    # https://www.totemmt.com/documents/TotemCam_Instructions_For_Use.pdf
    "Totem": {
        "0.5": (11.7, 17.1),
        "0.65": (13.8, 20.3),
        "0.8": (17, 25.0),
        "1": (20.9, 30.9),
        "1.25": (25.7, 38.1),
        "1.5": (31.6, 47),
        "1.8": (39.7, 58.1),
    }
}

bin_borders = set([c[0] for _, c in size_dict["Totem"].items()] +
                  [c[1] for _, c in size_dict["Totem"].items()] +
                  [c[0] for _, c in size_dict["BD C4"].items()] +
                  [c[1] for _, c in size_dict["BD C4"].items()])
bin_borders = sorted(list(bin_borders))


def make_camalot(brand: str, size: str) -> Camalot:
    if brand not in size_dict:
        raise ValueError(f"Unknown brand: {brand}")
    if size not in size_dict[brand]:
        raise ValueError(f"Unknown size: {size}")
    min, max = size_dict[brand][size]
    return Camalot(brand, size, min, max, int(1000./(max - min)))

def get_cam_count(camalots):
    def get_bin_counts(camalots, bin_borders):
        counts = [0] * (len(bin_borders) - 1)
        weights = [0] * (len(bin_borders) - 1)
        for camalot in camalots:
            for i in range(len(bin_borders) - 1):
                if camalot.min <= bin_borders[i] and camalot.max >= bin_borders[i + 1]:
                    counts[i] += 1
                    weights[i] += camalot.weight
        return counts, weights

    def get_bins_center_values(bin_borders, bin_counts):
        bin_centers = [(bin_borders[i] + bin_borders[i + 1]) / 2 for i in range(len(bin_borders) - 1)]
        bins = []
        for i in range(len(bin_borders) - 1):
            for j in range(bin_counts[i]):
                bins.append(bin_centers[i])
        return bins

    bin_counts, bin_weights = get_bin_counts(camalots, bin_borders)
    bin_vals = get_bins_center_values(bin_borders, bin_counts)
    bin_vals_weighted = get_bins_center_values(bin_borders, bin_weights)
    return bin_vals, bin_vals_weighted

def make_camalot_summary_plot():
    # create a list of camalots
    Alex_camalots = [
        make_camalot("BD C4", "0.5"),
        make_camalot("BD C4", "0.75"),
        make_camalot("BD C4", "1"),
        make_camalot("BD C4", "2"),
        make_camalot("Totem", "1.8"),
    ]

    Juno_camalots = [
        make_camalot("Totem", "0.5"),
        make_camalot("Totem", "0.8"),
        make_camalot("Totem", "1.25"),
        make_camalot("Totem", "1.8"),
        make_camalot("BD C4", "0.4"),
        make_camalot("BD C4", "0.5"),
        make_camalot("BD C4", "1"),
        make_camalot("BD C4", "3"),
    ]

    all_cams_count, all_cams_count_weighted = get_cam_count(Alex_camalots + Juno_camalots)
    alex_cams_count, alex_cams_count_weighted = get_cam_count(Alex_camalots)
    juno_cams_count, juno_cams_count_weighted = get_cam_count(Juno_camalots)

    # make 3 different plots on the same canvas
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(3, 1, figsize=(7, 12))
    plt.subplots_adjust(hspace=0.5)
    ax[0].hist(all_cams_count_weighted, bins=bin_borders, facecolor=(1,0,0,.4), edgecolor=(1,0,0,.01))
    ax[0].set_xlabel("Width (mm)")
    ax[0].set_ylabel("Count")
    ax[0].set_title("Juno + Alex")

    ax[1].hist(alex_cams_count_weighted, bins=bin_borders, facecolor=(1,0,0,.4), edgecolor=(1,0,0,.01))
    ax[1].set_xlabel("Width (mm)")
    ax[1].set_ylabel("Count")
    ax[1].set_title("Alex")

    ax[2].hist(juno_cams_count_weighted, bins=bin_borders, facecolor=(1,0,0,.4), edgecolor=(1,0,0,.01))
    ax[2].set_xlabel("Width (mm)")
    ax[2].set_ylabel("Count")
    ax[2].set_title("Juno")
    plt.show()

if __name__ == "__main__":
    make_camalot_summary_plot()