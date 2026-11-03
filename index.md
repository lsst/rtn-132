# Unrecognized blends in LSST DP1 and DP2 from the comparison with Euclid and HST

## Abstract

Unrecognized blends, objects that correspond to several truth sources, are a known issue in LSST data and a significant source of photometric error. In this technote, we present our methodology for identifying unrecognized blends in the LSST Data Preview 1 and 2 datasets (hereafter DP1 and DP2) by comparing them to high-resolution, space-based observations from Euclid Q1 and the Hubble Space Telescope (HST) in the Extended Chandra Deep Field South (ECDFS). By matching sources detected in the LSST data with those from the space telescopes, first by position and then by the overlap of their observed shapes, we quantify the fraction of sources that are blended in LSST but resolved in the space-based data. We find that up to 22% of sources in DP2 are unrecognized blends when compared to Euclid Q1 data for $23 < i < 24$. When compared to HST data, the fraction of unrecognized blends reaches up to 40% for the same magnitude range. Finally, we use the blending entropy $S_\text{b}$, which combines shape overlap with photometry, to quantify how ambiguous the galaxy association of each unrecognized blend is. This metric gives broadly consistent results for Euclid and HST down to the magnitude where Euclid, the shallower reference survey, becomes incomplete. This reconciles the two comparisons: at $i \simeq 23.5$, $19\%$ of DP2 sources have $S_\text{b} > 0.2$ when compared to Euclid and $16\%$ when compared to HST.


## Data

Blending, where multiple sources overlap on the sky, is expected to be a significant source of uncertainty for Stage-IV ground-based surveys like LSST {cite}`Melchior21`. Blended sources can often be identified and deblended. Unrecognized blends are a distinct case: objects that are detected as a single source in the survey data but that correspond to several distinct truth sources. Because the pipeline treats them as isolated objects, their properties (fluxes, colors, shapes) cannot be measured accurately or independently, and they are not flagged as blends. One way to study blending is to compare data from different telescopes with different resolutions and depths. Space-based observations have a higher angular resolution than ground-based ones because they are not affected by atmospheric turbulence, which broadens the point spread function (PSF), so blends unrecognized in ground-based images may be resolved in space-based images.

The Extended Chandra Deep Field South (ECDFS) is a deep survey field that has been observed by many telescopes at different wavelengths due to its low Galactic extinction {cite}`Lehmer05`. In this note, we use imaging of the ECDFS from three facilities.

- **Rubin LSST:** Rubin Observatory's Data Previews are early releases that precede LSST Data Release 1. Data Preview 1 (DP1) {cite}`RTN-095` is based on commissioning observations from the LSST Commissioning Camera (LSSTCam's smaller predecessor, ComCam) and includes ECDFS among its fields. Data Preview 2 (DP2) {cite}`RTN-115` is the first preview based entirely on data from the full LSST Science Camera (LSSTCam) and also covers the ECDFS. Both have a pixel scale of 0.2 arcsec/pixel. To access the LSST DP2 data, we use the Rubin Science Platform (RSP) and the `butler` API. The following parameters are used to specify the repository, collection, skymap, and catalog:

```python
repo='dp2_prep'
collection = 'LSSTCam/runs/DRP/DP2/v30_0_8/DM-55060/stage3'
skymap = 'lsst_cells_v2'
butler_cat = 'object'
```
- **Euclid Q1:** The Euclid Quick Data Release 1 (Q1) {cite}`EuclidQ1` is an early release of Euclid imaging and spectroscopy over ~63 deg² in three Euclid Deep Fields, one of which is ECDFS. We use the VIS optical imaging, which has a pixel scale of 0.1 arcsec/pixel. We use the final MER (MERge) catalog from Euclid Q1, which merges the VIS and NISP space-based imaging with external ground-based data to produce the combined multi-band source catalog.
- **HST:** The Hubble Space Telescope also imaged the ECDFS {cite}`HSTref`, providing high-resolution imaging with a pixel scale of 0.06 arcsec/pixel. We use the Hubble Legacy Fields (HLF) GOODS-South source catalog, which is a high-level science product derived from archival HST imaging.

```{figure} ./assets/plots/bandpasses.png
:name: fig-bandpasses
:alt: bandpasses
:width: 100%

Bandpasses of the LSST, Euclid and HST filters used in this study.
```
As shown in {numref}`fig-bandpasses`, the LSST, Euclid and HST filters used in this study cover overlapping wavelength ranges. The LSST $riz$ bands are the closest to the Euclid VIS band, and the LSST $i$ band is the closest to the HST F814W band.

The datasets also overlap spatially in the ECDFS, as shown in {numref}`fig-ecdfs`. The LSST DP2 and Euclid footprints cover the entire ECDFS field, while the HST footprint covers a smaller area within the ECDFS. Some areas of the LSST DP2 data are covered by only a single visit, which can lead to lower magnitude detections and artifacts. To avoid these effects we restrict the LSST data to a circular region of radius 2.1 degrees centered on the coordinates RA=53.05, Dec=-28.15 degrees, which is free of single visits and has a homogeneous depth.

```{figure} ./assets/plots/ecdfs_two_panel_vertical.png
:name: fig-ecdfs
:alt: ECDFS
:width: 90%

Top: One tenth of the detected galaxies in the ECDFS observed by LSST. The blue region corresponds to our region of study, chosen to avoid single-visit effects (lower magnitude detections and artifacts). The grey region is discarded due to the presence of single visits. The circle separating the two regions has a radius of 2.1 degrees and is centered on the coordinates RA=53.05, Dec=-28.15 degrees.
Bottom: One tenth of the detected galaxies in the ECDFS observed by LSST, Euclid and HST.
```

The Euclid ECDFS footprint has an area of 15.5 deg{sup}`2` and contains 5,328,489 galaxies detected in the VIS band and 2,416,305 objects detected in the LSST DP2 dataset.\
The HST ECDFS footprint has an area of 0.18 deg{sup}`2` and contains 165,776 galaxies detected in the F814W band and 33,240 objects detected in the LSST DP2 dataset.

In the following sections, we will refer to sources detected in the LSST DP datasets as `objects` and to sources detected in the Euclid and HST datasets as (reference) `galaxies`. We will also refer to the objects that are associated with more than one reference galaxy as `blends`. Unless stated otherwise, all plots are for the LSST DP2 dataset. The results for the LSST DP1 dataset are similar and can be found in the Appendix of this technote.

## Methods

The pipeline described below is available at [https://github.com/LSSTDESC/copaings](https://github.com/LSSTDESC/copaings).

### Matching LSST DP catalogs with Euclid and HST

We match the sources detected in the LSST DP datasets with those from Euclid and HST using a two-step process:

1. Friends-of-friends (FoF) catalog matching {cite}`FoFMatching`: pairs of "friends" within a specified linking length are connected iteratively and transitively, and their associated groups are merged. It starts with each object as its own group, then recursively merges groups if any member of one group is within the linking length of any member of another. The choice of linking length defines the scale of the resulting structures. We chose a linking length of 2 arcsec to make coarse groups, in which all elements are initially connected to each other.
2. Ellipse Overlap Test (EOT): For each element (object/galaxy) in each group, we define an elliptical footprint computed from the semi-major and semi-minor axes and the position angle of the detection. For that footprint, we also account for the effect of the local LSST PSF by convolving the ellipse with it. Starting from densely connected FoF groups, we then test whether the ellipses of each pair of elements overlap. If there is no overlap between two elements, we remove their link. If non-overlapping subsets are found, we split the group into subgroups until all elements in each group are connected through overlapping ellipses. We discard groups made of a single element (object or galaxy).

Adding the EOT step after the FoF matching makes our matching independent of the linking length choice, provided the linking length is large enough to capture all overlapping elements. The result of this matching is a set of groups where each group contains one or more objects and one or more galaxies. Elements within a group overlap, at least transitively.
From this matching, we compute the number of objects and galaxies per group, as shown in {numref}`fig-nm-groups`.

```{figure} ./assets/plots/detect_counts_cbar_on_bottom_vertical.png
:name: fig-nm-groups
:alt: N-M groups
:width: 75%

Results of the LSST–Euclid and LSST–HST cross-matching with the FoF+EOT method. Each bin of the 2D histogram counts the groups with a given number of objects (LSST detections, in columns) and galaxies (Euclid detections, top, or HST detections, bottom, in rows). The colorbar indicates the number of groups in each bin.
```

We call unrecognized blends the groups having more galaxies than objects, which correspond to the lower-left part of {numref}`fig-nm-groups`. The fraction of unrecognized blends is higher for HST than for Euclid due to the higher resolution and depth of the HST data. Using this plot, we estimate that 13.8% of LSST DP2 objects are unrecognized blends when compared to Euclid and 38.7% when compared to HST.

### Blending entropy

For each object detected in the LSST DP, we assign a blending entropy value {cite}`Ramel26` that quantifies how ambiguous its galaxy association is. The blending entropy for a given wavelength band is defined as:

```{math}
S_{\text{b},o} = -\sum_{\text{g}\in\text{gal}} p_\text{og} \ln(p_\text{og}) \ge 0 \quad \text{with} \quad p_\text{og} \propto \left\langle \text{o},\text{g} \right\rangle \exp\left(-\left|  m_\text{o}-m_\text{g}\right|\right)
```

$p_\text{og}$ is the matching probability of object $o$ with galaxy $g$, given by the intersection-over-union $\left\langle \text{o},\text{g} \right\rangle$ of the two ellipses --- the area they share divided by the area they cover together, ranging from 0 (disjoint) to 1 (identical) --- weighted by an exponential factor in their magnitude difference. The probabilities are normalized per object so that $\sum_{\text{g}\in\text{gal}}p_\text{og} = 1$. Systems with one object and one galaxy have a matching probability of 1 and a blending entropy of 0. The blending entropy ranges from 0, meaning no ambiguity, to $\ln N$, meaning maximum ambiguity, where $N$ is the number of galaxies in the overlapping group.

```{figure} ./assets/high_sb_blend_lsst_euclid_hst.png
:name: fig-high-sb-image
:alt: High Sb

Example of a high-$S_\text{b}$ blend. Top: LSST DP2 cutout with $i,r,g$ bands corresponding to red, green and blue respectively. Middle: Euclid VIS. Bottom: HST F775W. The object from the LSST detection is represented by the blue ellipse; galaxies from the Euclid and HST detections are represented by the orange and green ellipses, respectively. The Euclid and HST ellipses were convolved with the LSST PSF to account for the difference in resolution.
```

{numref}`fig-high-sb-image` shows an example of a high-blending-entropy system with one object and two galaxies. The object overlaps with both galaxies and has a similar magnitude to both of them, making its association with either of the two galaxies ambiguous.
The blending entropy for this object is $S_\text{b} = 0.66$.

```{figure} ./assets/low_sb_blend_lsst_euclid_hst.png
:name: fig-low-sb-image
:alt: Low Sb

Example of a low-$S_\text{b}$ blend. Top: LSST DP2 cutout with $i,r,g$ bands corresponding to red, green and blue respectively. Middle: Euclid VIS. Bottom: HST F775W. The object from the LSST detection is represented by the blue ellipse; galaxies from the Euclid and HST detections are represented by the orange and green ellipses, respectively. The Euclid and HST ellipses were convolved with the LSST PSF to account for the difference in resolution.
```

Conversely, {numref}`fig-low-sb-image` shows an example of a low-blending-entropy system with one object and two galaxies. One of the Euclid detections overlaps almost entirely with the LSST detection, while the other overlaps only partially and has a lower magnitude. The LSST detection is unambiguously associated with the low magnitude Euclid detection.
The blending entropy for this object is $S_\text{b} = 0.08$.

The blending entropy requires comparing magnitudes measured in the same band. The LSST DP datasets include observations in the $ugrizy$ bands, while Euclid and HST observe in the VIS and F814W bands ({numref}`fig-bandpasses`). We model the VIS and F814W magnitudes as functions of the closest LSST bands: the $griz$ bands for the LSST-Euclid comparison and the $i$ band for the LSST-HST comparison. The fit coefficients are computed using only one-to-one systems, since their photometry is cleaner than that of many-to-one systems. The fit is then applied to every object in the LSST DP datasets.


For Euclid, we use the following fit, based on the colors:

$$
\text{VIS}_{\text{fit}} = r_{\text{term}} + c_{g-r} \cdot (g - r) + c_{r-i} \cdot (r - i) + c_{i-z} \cdot (i - z)
$$

We define $r_{\text{term}}$ as a piecewise linear function of $r$:

- If $r \leq 22$:
  $r_{\text{term}} = a_0^{\text{low}} + c_r^{\text{low}} \cdot r$

- If $r > 22$: $\,r_{\text{term}} = a_0^{\text{high}} + c_r^{\text{high}} \cdot r$
  where we define $a_0^{\text{high}} = a_0^{\text{low}} + (c_r^{\text{low}} - c_r^{\text{high}}) \cdot 22$ to ensure continuity at $r = 22$.

For HST, we use a linear fit to the $i$-band magnitude:
$\text{F814W}_{\text{fit}} = c_0 + c_{i} \cdot i$

The fitted coefficients are given in {ref}`appendix-fit-coeffs`.

```{figure} ./assets/plots/duo_fit_plot.png
:name: fig-duo-fit
:alt: Duo fit plot
:width: 100%

Verification of the VIS magnitude and F814W magnitude fits. Left: The x-axis is the measured VIS magnitude from Euclid and the y-axis is the predicted VIS magnitude from the LSST DP2 photometry. Right: The x-axis is the measured F814W magnitude from HST and the y-axis is the predicted F814W magnitude from the LSST DP2 photometry. The colorbar indicates the number of objects in each bin. The red line shows $x=y$.
```

{numref}`fig-duo-fit` shows that the fits provide a reasonable approximation of the space-based magnitudes from the LSST DP2 photometry. For each object in the LSST DP datasets, we can therefore compute the blending entropy for either Euclid, using the VIS fit from the $griz$ bands, or HST, using the F814W fit from the $i$ band.



## Results

From the matching of the LSST DP2 catalog with the Euclid and HST catalogs, we can compute the fraction of objects that belong to blends as a function of magnitude. The $S_\text{b} > 0$ cut effectively removes objects with $S_\text{b} = 0$, which by definition of the blending entropy belong to one-to-one systems. We also compute the fraction of high-blending-entropy objects, which are those with $S_\text{b} > 0.2$, as a function of magnitude. This cut removes all systems whose galaxy association is unambiguous, leaving only problematic blends in the dataset. See {cite:t}`Ramel26` for a detailed justification of this threshold.

```{figure} ./assets/plots/duo_plot_mag_highsb.png
:name: fig-mag-highsb
:alt: Fraction of unrecognized blends as a function of i-band magnitude
:width: 100%

Top: Distribution of detection magnitudes for LSST (blue), Euclid (orange) and HST (green) in ECDFS. Since the observation bands of these telescopes do not cover the same wavelength ranges, a fit was made to compare them consistently using the LSST $i$-band as a reference. Bottom: Fraction of high-$S_\text{b}$ blends in LSST DP2 with either Euclid or HST as reference space-based data.
```

{numref}`Fig. %s-a) <fig-mag-highsb>` shows the magnitude distribution of each instrument and 7b the fraction of matched objects meeting a minimum blending entropy cut-off. We see that the HST observations are much deeper than both LSST and Euclid.
{numref}`Fig. %s-b) <fig-mag-highsb>` shows the fraction of overlapping objects ($S_\text{b} > 0$) and the fraction of high-blending-entropy objects ($S_\text{b} > 0.2$) as a function of magnitude. The fraction of overlapping objects is higher for HST than for Euclid, which is expected since HST has a higher resolution and depth than Euclid. In these cases, single LSST objects often consist of a bright galaxy and a much fainter one that HST detects but Euclid does not. Moreover, the fraction of overlapping objects increases with magnitude for both Euclid and HST, as expected since fainter objects are more likely to be blended. This trend breaks down at $i \simeq 23.5$ with Euclid as the reference; we interpret this as Euclid's detection limit, beyond which it cannot detect the fainter object of the blend. The fraction of unrecognized blends exceeds 20% for Euclid, which is consistent with the results reported by {cite:t}`SITCOMTN-128` and {cite:t}`Troxel23`.

After applying the $S_\text{b}>0.2$ cut, we find that the fraction of problematic blends (those with an ambiguous match and therefore high $S_\text{b}$) is consistent between the two reference surveys up to the Euclid magnitude limit.
This explains the discrepancy between the two curves in {numref}`Fig. %s-b) <fig-mag-highsb>` for $i < 23.5$: the fraction of unrecognized blends is higher for HST because it detects more faint galaxies that are not detected by Euclid, but these blends are not ambiguous in their galaxy association: the LSST detection is unambiguously associated with the brighter galaxy of the blend.

## Discussion

In this technote, we matched LSST DP2 objects to Euclid Q1 and HST galaxies in the ECDFS with a FoF + EOT procedure and found that unrecognized blends make up 13.8% of objects when using Euclid as space-based reference data and 38.7% when using HST as reference. We used the blending entropy $S_\text{b}$ to show that the two reference surveys give consistent fractions of ambiguous blends up to the Euclid magnitude limit.

The blend fractions reported here apply to DP2 and should be regarded as an upper bound for later LSST data releases. The image quality in DR1 is expected to be significantly better than in DP2, which reduces the overlap between neighboring sources and should therefore yield lower unrecognized blend fractions {cite}`Bosch18,Sanchez21`.
We are working on a follow-up study that repeats this analysis as a function of image quality to quantify directly how the blend fractions improve as the delivered image quality evolves.

Unrecognized blends are an important systematic for weak lensing, since the shapes measured for blended systems are biased and this bias propagates to the shear estimates {cite}`MacCrann22`. The blend fractions measured here are therefore directly relevant to DESC shear calibration, and an improvement in image quality between DP2 and DR1 should translate into a smaller blending-induced calibration correction.


## Appendix

(appendix-fit-coeffs)=
### Coefficients of the magnitude fits

Euclid VIS fit:

- $a_0^{\text{low}} = 5.666$
- $a_0^{\text{high}} = 3.972$
- $c_r^{\text{low}} = 0.8145$
- $c_r^{\text{high}} = 0.892$
- $c_{g-r} = 0.005$
- $c_{r-i} = -0.873$
- $c_{i-z} = -0.006$

HST F814W fit:

- $c_0 = -1.249$
- $c_i = 1.005$

## References

```{bibliography}
```


