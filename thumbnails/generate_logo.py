# %%

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import s3fs
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap, Normalize

THUMBNAIL_DIR = Path("../thumbnails")
THUMBNAIL_DIR.mkdir(exist_ok=True)

URL = "https://js2.jetstream-cloud.org:8001/"
fs = s3fs.S3FileSystem(anon=True, client_kwargs=dict(endpoint_url=URL))

# Short period → blue; long period → red. Saturated for the dark background.
RAINBOW_STOPS = [
    "#3b82f6",
    "#06b6d4",
    "#22d3ee",
    "#4ade80",
    "#a3e635",
    "#facc15",
    "#fb923c",
    "#f87171",
    "#ef4444",
]
RAINBOW = LinearSegmentedColormap.from_list(
    "rainbow_logo", RAINBOW_STOPS, N=256)


BG = "#0f1724"
WHITE = "#f4f7fb"

# %%

olr_noaa_store = s3fs.S3Map(root="pythia/olr_noaa.zarr", s3=fs, check=False)
olr_noaa = xr.open_zarr(olr_noaa_store)
olr_noaa = olr_noaa.rename_vars({"__xarray_dataarray_variable__": "olr"})
olr_noaa = olr_noaa.chunk({"time": -1})
olr_noaa = olr_noaa.interpolate_na(dim="time", method="linear")

lat_select = 0
lon_select = 70
olr_series = olr_noaa["olr"].sel(
    lat=lat_select, lon=lon_select, method="nearest")
series = olr_series.load().values.astype(float)

print(
    f"OLR at (lat={lat_select}, lon={lon_select}): {len(series):,} daily samples")


# %%
n_time = len(series)
n_harmonics = 4
year_period = 365.25  # days

t = np.arange(n_time)
X = np.ones((n_time, 2 * n_harmonics + 1))
for i in range(1, n_harmonics + 1):
    X[:, 2 * i - 1] = np.sin(i * 2 * np.pi * t / year_period)
    X[:, 2 * i] = np.cos(i * 2 * np.pi * t / year_period)

coeffs = np.linalg.lstsq(X, series, rcond=None)[0]
annual_cycle = X @ coeffs
anomalies = series - annual_cycle
# %%


def power_spectrum(series, dt=1.0):
    """Return positive-frequency periods (days) and explained variance (%)."""
    x = series - np.mean(series)
    n = len(x)
    freqs = np.fft.rfftfreq(n, d=dt)
    coeffs = np.fft.rfft(x)
    power = np.abs(coeffs) ** 2

    var = np.var(x)
    power_norm = 100.0 * power / power.sum() if power.sum() > 0 else power

    with np.errstate(divide="ignore"):
        periods = np.where(freqs > 0, 1.0 / freqs, np.inf)

    mask = freqs > 0
    return periods[mask], power_norm[mask]


# %%
period, power = power_spectrum(anomalies)

plt.semilogx(period, power)


def draw_rainbow_spectrum(ax, x, y):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_color("#334155")
    log_x = np.log10(x)
    norm = Normalize(vmin=log_x.min(), vmax=log_x.max())

    # Gouraud shading on native FFT bins: smooth rainbow, sharp spectral peaks.
    mesh_x = np.vstack([x, x])
    mesh_y = np.vstack([np.zeros(len(x)), y])
    mesh_c = np.vstack([log_x, log_x])
    ax.pcolormesh(
        mesh_x,
        mesh_y,
        mesh_c,
        cmap=RAINBOW,
        norm=norm,
        shading="gouraud",
        antialiased=True,
        zorder=2,
    )

    ax.set_xscale("log")
    ax.set_xlim(x.min(), x.max())
    # Hide y-axis ticks and labels, but keep the grid
    ax.tick_params(
        axis="y",
        which="both",
        left=False,       # no tick marks
        labelleft=False,  # no tick labels
    )

    ax.set_xlabel("Period ", color="#94a3b8", fontsize=10)
    ax.set_ylabel("Power", color="#94a3b8", fontsize=10)
    ax.tick_params(colors="#94a3b8", labelsize=8)
    ax.grid(True, which="both", color="#1e293b", lw=0.6, alpha=0.9)


def save_logo(fig, path, dpi=200):
    fig.savefig(path, facecolor=BG, dpi=dpi)


def make_logo(x, y):
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(BG)
    draw_rainbow_spectrum(ax, x, y)
    plt.tight_layout()
    return fig


fig = make_logo(period, power)
# save_logo(fig, "spectral_analysis.png", dpi=150)
#%%