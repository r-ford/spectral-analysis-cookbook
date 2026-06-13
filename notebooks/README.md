# Overview

A cookbook that shows how to *reproduce* the Real-time Multivariate MJO (RMM) index of [Wheeler and Hendon (2004)](https://doi.org/10.1175/1520-0493%282004%29132%3C1917:AARMMI%3E2.0.CO;2) using Python. The **Madden–Julian Oscillation (MJO)** is the most important mode of tropical variability on the intraseasonal time scale [(Zhang, 2005)](https://doi.org/10.1029/2004RG000158). The steps to compute the RMM index, used to monitor and diagnose the MJO state, are simple and represent a great opportunity to learn different tools used in atmospheric data analysis: **Fourier analysis, spectral filtering, Empirical Orthogonal Functions (EOFs), and wavelet space–time spectra filtering**.

MJO's global-scale circulation cells

## What is New Compared to Existing Cookbooks

Project Pythia already has cookbooks about EOFs and about wavelets. What this cookbook adds is:

- A **single example** (the MJO) that uses Spectral filtering, EOFs, and the regression methods together.
- A clear description of the **practical choices** :
  - how to compute anomalies based on harmonics of the annual cycle
  - how to normalize variables with different units
  - how to build the combined state vector for the EOF, also useful for Time-Extended EOF Analysis
  - how to optimize the computation of Principal Component Analysis based on the chosen **covariance matrix**. Key choice for performing the **RMM Analysis**.

## Outline

### Part I: Methods Primers

#### Notebook 1: Fourier Analysis and Spectral Filtering

*Goal.* Learn how to take the Fourier transform of a climate time series, how to read its power spectrum, and how to design a filter from it.

- A short review of the discrete Fourier transform: amplitude, phase, Nyquist frequency, and [spectral leakage (Gibbs Phenomenon)](Gibbs_phenomenon.ipynb).
- Plot the spectrum of a 1-D time series, for example, a single grid point of SST or OLR.
- Remove the **annual cycle** of the selected time series in two ways:
  - by subtracting a smoothed daily climatology
  - by filtering out the harmonics of one cycle per year.
- Design **high-pass, low-pass, and band-pass** filters in frequency space.
- Apply filters to a 1-D time series and then to a 3-D field (daily SST as an example).
- **Variance budget.** Compute a map of the fraction of total variance that is explained by each time scale:
  - Interannual (2–7 years)
  - Annual (around 365 days)
  - Semiannual (around 180 days)
  - Intraseasonal (20–90 days)

#### Notebook 2: Empirical Orthogonal Functions (EOFs)

*Goal.* Build EOFs step by step from the covariance matrix (the same procedure is known as Principal Component Analysis, or PCA, in other fields), understand what the eigenvectors and eigenvalues mean, and see how the preprocessing changes the way we read the result.

We build on the existing [EOF cookbook](https://projectpythia.org/eofs-cookbook/). Here we focus on the choice that matters most for the RMM: **how to build the covariance matrix**. Let $X$ be the data matrix, with rows corresponding to time and columns to space. The covariance can be formed in two ways:

- $X^{T} X$:  a *space × space* matrix. Its eigenvectors are the spatial EOFs.
- $XX^{T}$: a *time × time* matrix. Its eigenvectors are the principal components (PCs).

Both products share the same non-zero eigenvalues, so the two routes give the same answer. The choice is mostly practical: we pick the smaller of the two matrices to keep the computation cheap.

- [A small 2-D example to see what the leading patterns look like](EOF_2D.ipynb).
- A 3-D example with one variable, for example, tropical SST anomalies.
  - Do the analysis with both versions of the covariance matrix and check that the EOFs, PCs, and explained variances agree.

### Part II: Building the RMM Index

#### Notebook 3: RMM Index

- Background:
  - What the MJO is, where we see it, and which variables show it best.
  - Explain the RMM INDEX
  - A quick view of the recipe: variables, latitude band, filter, EOF, projection.
- Read the information:
  - Read OLR, U850, and U200 and select the 15°S–15°N band.
- Preprocessing:
  - Compute **daily anomalies** by removing the annual cycle and the first 4 harmonics. This uses what we learned in Notebook 1.
  - Apply a **20–90-day band-pass filter** to keep only the intraseasonal signal.
  - Take the **meridional mean** to obtain three 2-D fields with dimensions *(time, longitude)*.
  - **Standardize** each field by its own standard deviation in the equatorial band, so that no single variable dominates the EOF.
- EOF Analysis:
  - Build the "extended" state vector by joining standardized OLR, U850, and U200 along the longitude axis.
  - Compute the EOFs and save the eigenvectors, principal components, and explained variance.
  - Store the results in an `xarray.Dataset` so they are easy to use later.
- Compare the results with Wheeler and Hendon (2004):
  - **EOF patterns** for the two leading modes.
  - **PC time series**, called RMM1 and RMM2.
  - **Phase diagram** with the eight MJO phases.

#### Notebook 4: Regression onto the Principal Components

- Regress each global 3-D field (OLR, U850, U200, geopotential height,...) on RMM1 and RMM2.
- Reconstruct the MJO life cycle by taking linear combinations of the two regression maps:
`-PC2`, `(PC1 - PC2)/sqrt(2)`, `PC1`, `(PC1 + PC2)/sqrt(2)`, `PC2`.
- Compare the reconstructed maps with Wheeler and Hendon (2004) and Adames and Wallace (2014).