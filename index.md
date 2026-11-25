# Unrecognized blends in LSST DP2 from the comparison with Euclid DR1 and HST

## Abstract

Unrecognized blends, objects that correspond to several truth sources, are a known issue in LSST data and a significant source of photometric error. In this technote, we identify unrecognized blends in the LSST Data Preview 2 (DP2) dataset by comparing it to high-resolution, space-based observations from Euclid Data Release 1 (DR1) and the Hubble Space Telescope (HST) in the Extended Chandra Deep Field South (ECDFS). By matching sources detected in the LSST data with those from the space telescopes, first by position and then by the overlap of their observed shapes, we quantify the fraction of LSST objects that are unrecognized blends, i.e. blended in LSST but resolved in the space-based data. We find that $18.2\%$ of the LSST DP2 objects with a Euclid counterpart are unrecognized blends, i.e. correspond to more Euclid galaxies than LSST detects, and $46.8\%$ with HST as the reference. Since this binary classification depends strongly on the depth of the reference survey, we then use the blending entropy $S_\text{b}$, a continuous metric that combines shape overlap with photometry, to quantify how ambiguous the galaxy association of each blend is.
The fraction of DP2 objects that are blends ($S_\text{b} > 0$) peaks near $i \simeq 24$ at $\simeq 26\%$ with Euclid and $\simeq 42\%$ with HST but the fraction of ambiguous blends ($S_\text{b} > 0.2$) is comparable for the two references down to the magnitude where Euclid, the shallower reference survey, becomes incomplete, reaching $\simeq 20\%$ of ambiguous blends at $i \simeq 24$ with either reference survey.
<!-- This metric gives comparable results for Euclid and HST down to the magnitude where Euclid, the shallower reference survey, becomes incomplete. This reconciles the two comparisons: at $i \simeq 24$, the fraction of DP2 objects having $S_\text{b} > 0.2$  is $20\%$ when compared to either Euclid or HST. This fraction is expected to decrease with the better image quality of LSST Data Release 1, and is directly relevant to the calibration of blending effects in weak-lensing analyses. -->


## Introduction

Blending, where multiple sources visually overlap on the sky, is expected to be a significant source of uncertainty for Stage-IV ground-based surveys like LSST {cite}`Chang13,Dawson16,Melchior21`. Blended sources can often be identified and deblended. Unrecognized blends are a distinct case: objects that are detected as a single source in the survey data but that correspond to several distinct truth sources. Because the pipeline treats them as isolated objects, their properties (fluxes, colors, shapes) cannot be measured accurately or independently, and they are not flagged as blends. One way to study blending is to compare data from different telescopes with different resolutions and depths. Space-based observations have a higher angular resolution than ground-based ones because they are not affected by atmospheric turbulence, which broadens the point spread function (PSF), so blends unrecognized in ground-based images may be resolved in space-based images.

In this note, we use Euclid DR1 and HST imaging of the Extended Chandra Deep Field South to measure the fraction of unrecognized blends in the LSST DP2 dataset as a function of magnitude, and we quantify how ambiguous these blends are with the blending entropy {cite}`Ramel26`, a continuous metric that, unlike a binary match, is largely insensitive to the depth of the reference survey.

## Data

The Extended Chandra Deep Field South (ECDFS) is a deep survey field that has been observed by many telescopes at different wavelengths due to its low Galactic extinction {cite}`Lehmer05`. In this note, we use imaging of the ECDFS from three facilities.

- **Rubin LSST:** Rubin Observatory's Data Preview 2 (DP2) {cite}`RTN-115` is an early release based on commissioning observations from the LSST Science Camera (LSSTCam) with a a pixel scale of 0.2 arcsec/pixel. To access the LSST DP2 data on ECDFS, we use the Rubin Science Platform (RSP) and the `butler` API. The following parameters are used to specify the repository, collection, skymap, and catalog:

```python
repo='dp2_prep'
collection = 'LSSTCam/runs/DRP/DP2/v30_0_8/DM-55060/stage3'
skymap = 'lsst_cells_v2'
butler_cat = 'object'
```
- **Euclid DR1:** The Euclid Data Release 1 (DR1) {cite}`EuclidDR1` is the first major release of Euclid imaging and spectroscopy, which includes the part of the ECDFS covered by the Euclid Deep Field Fornax. We use the VIS optical imaging, which has a pixel scale of 0.1 arcsec/pixel. We use the final MER (MERge) catalog from Euclid DR1, which merges the VIS and NISP space-based imaging with external ground-based data to produce the combined multi-band source catalog.
- **HST:** The Hubble Space Telescope also imaged the ECDFS {cite}`HSTref`, providing high-resolution imaging with a pixel scale of 0.06 arcsec/pixel. We use the Hubble Legacy Fields (HLF) GOODS-South source catalog, which is a high-level science product derived from archival HST imaging.

```{figure} ./assets/plots/bandpasses.png
:name: fig-bandpasses
:alt: bandpasses
:width: 100%

Bandpasses of the LSST, Euclid and HST filters used in this study.
```
As shown in {numref}`fig-bandpasses`, the LSST, Euclid and HST filters used in this study cover overlapping wavelength ranges. The LSST $riz$ bands are the closest to the Euclid VIS band, and the LSST $i$ band is the closest to the HST F814W band.

The datasets also overlap spatially in the ECDFS, as shown in {numref}`fig-ecdfs`. The LSST DP2 footprint covers the entire ECDFS field, while the HST and Euclid footprints cover a smaller area within the ECDFS. Some areas of the LSST DP2 data are covered by only a single visit, which can lead to shallower detections and artifacts. However, the Euclid and HST footprints are free of single visits, so we restrict our analysis to the area of overlap between the three datasets to avoid these effects. The LSST DP2 footprint is also uniform in that overlapping area.

```{figure} ./assets/plots/DR1_ecdfs_two_panel_vertical.png
:name: fig-ecdfs
:alt: ECDFS
:width: 90%

Top: Sky density of LSST DP2 galaxies in the ECDFS field. The map shows all 3.6 million objects with `i_extendedness = 1`. the colour gives the number of galaxies per cell. The density drops in the shallower outer tracts. The circle separating the two regions has a radius of 1.6 degrees and is centered on the coordinates RA=53.00, Dec=-28.15 degrees.
Bottom: One tenth of the detected galaxies in the ECDFS observed by LSST, Euclid and HST.
```
The Euclid ECDFS footprint has an area of 8.161 deg{sup}`2` and contains 3,804,671 galaxies detected in the VIS band, of which 1,999,739 have a counterpart in the LSST DP2 dataset.
The HST ECDFS footprint has an area of 0.129 deg{sup}`2` and contains 118,612 galaxies detected in the F814W band, of which 47,657 have a counterpart in the LSST DP2 dataset.

In the following sections, we will refer to sources detected in the LSST DP2 dataset as *objects* and to sources detected in the Euclid and HST datasets as (reference) *galaxies*. We call *unrecognized blends* the objects that belong to a matched group (see Methods) containing more reference galaxies than LSST objects: in such groups, LSST detected fewer sources than the space-based reference. More generally, we call *blends* the objects whose ellipse overlaps those of at least two reference galaxies, i.e. objects with a blending entropy $S_\text{b} > 0$.

## Methods

The pipeline described below is available at [https://github.com/LSSTDESC/copaings](https://github.com/LSSTDESC/copaings). The plots in this technote were generated using this same code.

### Matching LSST DP2 catalog with Euclid and HST

We match the sources detected in the LSST DP2 dataset with those from Euclid and HST using a two-step process:

1. Friends-of-friends (FoF) catalog matching {cite}`FoFMatching`: pairs of "friends" within a specified linking length are connected iteratively and transitively, and their associated groups are merged. It starts with each object as its own group, then recursively merges groups if any member of one group is within the linking length of any member of another. The choice of linking length defines the scale of the resulting structures. We chose a linking length of 3 arcsec to make coarse groups, in which all elements are initially connected to each other. This length is larger than the typical size of the PSF-convolved ellipses, and we checked that larger linking lengths have a negligible impact on our results.
2. Ellipse Overlap Test (EOT): For each element (either an object or a galaxy) in each group, we define an elliptical footprint computed from the semi-major and semi-minor axes and the position angle of the detection. For that footprint, we also account for the effect of the local LSST PSF by convolving the ellipse with it. Starting from densely connected FoF groups, we perform a geometric test to determine whether the ellipses of each pair of elements overlap. If there is no overlap between two elements, we remove their link. If non-overlapping subsets are found, we split the group into subgroups until all elements in each group are connected through overlapping ellipses. We discard groups made of a single element (object or galaxy).

Adding the EOT step after the FoF matching makes our matching independent of the linking length choice, provided the linking length is large enough to capture all overlapping elements. The result of this matching is a set of groups where each group contains one or more objects and one or more galaxies. Elements within a group overlap, at least transitively.
From this matching, we compute the number of objects and galaxies per group, as shown in {numref}`fig-nm-groups`.

```{figure} ./assets/plots/DR1_detect_counts_cbar_on_bottom_vertical.png
:name: fig-nm-groups
:alt: N-M groups
:width: 75%

Results of the LSST–Euclid and LSST–HST cross-matching with the FoF+EOT method. Each bin of the 2D histogram counts the groups with a given number of objects (LSST detections, in columns) and galaxies (Euclid detections, top, or HST detections, bottom, in rows). The number in each cell is the number of groups; the percentage is that number divided by the total number of groups shown. The colorbar indicates the number of groups in each bin.
```

Groups with more galaxies than objects, in the lower-left part of {numref}`fig-nm-groups`, are those in which LSST detects fewer sources than the reference survey; the LSST objects in these groups are the unrecognized blends.

### Blending entropy

The matching described above provides a binary classification of LSST objects, which depends strongly on the depth of the reference survey: a deeper survey detects more faint companions and therefore finds more unrecognized blends, even when these companions contribute little to the flux of the LSST object. To obtain a blending metric that is continuous and largely insensitive to the depth of the reference survey, we assign to each object detected in the LSST DP a blending entropy value {cite}`Ramel26` that quantifies how ambiguous its galaxy association is. The blending entropy for a given wavelength band is defined as:

```{math}
S_{\text{b},o} = -\sum_{\text{g}\in\text{gal}} p_\text{og} \ln(p_\text{og}) \ge 0 \quad \text{with} \quad p_\text{og} \propto \left\langle \text{o},\text{g} \right\rangle \exp\left(-\left|  m_\text{o}-m_\text{g}\right|\right)
```

$p_\text{og}$ is the matching probability of object $o$ with galaxy $g$, given by the intersection-over-union $\left\langle \text{o},\text{g} \right\rangle$ of the two ellipses --- the area they share divided by the area they cover together, ranging from 0 (disjoint) to 1 (identical) --- weighted by an exponential factor in their magnitude difference. The probabilities are normalized per object so that $\sum_{\text{g}\in\text{gal}}p_\text{og} = 1$. Systems with one object and one galaxy have a matching probability of 1 and a blending entropy of 0. The blending entropy ranges from 0, meaning no ambiguity, to $\ln N$, meaning maximum ambiguity, where $N$ is the number of galaxies in the overlapping group. Because each galaxy is weighted in $p_\text{og}$ by its magnitude difference with the object, faint companions contribute little to the blending entropy, as long as the reference survey is deep enough to detect the galaxies that dominate the flux of the object.

```{figure} ./assets/DR1_high_sb_blend_lsst_euclid_hst.png
:name: fig-high-sb-image
:alt: High Sb

Example of a high-$S_\text{b}$ blend. Upper left: LSST DP2 cutout with $i,r,g$ bands corresponding to red, green and blue respectively. Upper right: Euclid VIS. Bottom left: HST F814W. The object from the LSST detection is represented by the blue ellipse; galaxies from the Euclid and HST detections are represented by the orange and green ellipses, respectively. The Euclid and HST ellipses were convolved with the LSST PSF to account for the difference in resolution.
```

{numref}`fig-high-sb-image` shows an example of a high-blending-entropy system with one object and two galaxies. The object overlaps with both galaxies and has a similar magnitude to both of them, making its association with either of the two galaxies ambiguous.
The blending entropy for this object, with Euclid as the reference, is $S_\text{b} = 0.65$ and $S_\text{b} = 0.80$ with HST as the reference.

```{figure} ./assets/DR1_low_sb_blend_lsst_euclid_hst.png
:name: fig-low-sb-image
:alt: Low Sb

Example of a low-$S_\text{b}$ blend. Upper left: LSST DP2 cutout with $i,r,g$ bands corresponding to red, green and blue respectively. Upper right: Euclid VIS. Bottom left: HST F814W. The object from the LSST detection is represented by the blue ellipse; galaxies from the Euclid and HST detections are represented by the orange and green ellipses, respectively. The Euclid and HST ellipses were convolved with the LSST PSF to account for the difference in resolution.
```

Conversely, {numref}`fig-low-sb-image` shows an example of a low-blending-entropy system with one object and two galaxies. One of the Euclid detections overlaps almost entirely with the LSST detection, while the other overlaps only partially and is more than one magnitude fainter. The LSST detection is therefore unambiguously matched with the brighter Euclid detection.
The blending entropy for this object, with Euclid as the reference, is $S_\text{b} = 0.02$ and $S_\text{b} = 0.15$ with HST as the reference.

The blending entropy compares the magnitude $m_\text{o}$ of each LSST object with the magnitudes $m_\text{g}$ of the reference galaxies, which requires both to be measured in the same band. Since Euclid and HST observe in the VIS and F814W bands, which have no exact LSST counterpart ({numref}`fig-bandpasses`), we predict for each LSST object its VIS or F814W magnitude from its LSST photometry, using the closest LSST bands: $griz$ for Euclid and $i$ for HST. The relation between the LSST magnitudes of an object and the measured VIS or F814W magnitude of its reference galaxy is fitted on one-to-one systems only, where both measurements refer to the same galaxy and the photometry is cleanest. This relation is then applied to every object in the LSST DP2 dataset, and the predicted magnitude is used as $m_\text{o}$ in the definition of $S_\text{b}$.


For Euclid, the predicted VIS magnitude depends on the $r$-band magnitude and on the $g-r$, $r-i$ and $i-z$ colors:

$$
\text{VIS}_{\text{fit}} = r_{\text{term}} + c_{g-r} \cdot (g - r) + c_{r-i} \cdot (r - i) + c_{i-z} \cdot (i - z)
$$

We define $r_{\text{term}}$ as a piecewise linear function of $r$:

- If $r \leq 22$:
  $r_{\text{term}} = a_0^{\text{low}} + c_r^{\text{low}} \cdot r$

- If $r > 22$: $\,r_{\text{term}} = a_0^{\text{high}} + c_r^{\text{high}} \cdot r$
  where we define $a_0^{\text{high}} = a_0^{\text{low}} + (c_r^{\text{low}} - c_r^{\text{high}}) \cdot 22$ to ensure continuity at $r = 22$.

For HST, the predicted F814W magnitude is a linear function of the $i$-band magnitude:
$\text{F814W}_{\text{fit}} = c_0 + c_{i} \cdot i$

The fitted coefficients are given in {ref}`appendix-fit-coeffs`.

```{figure} ./assets/plots/DR1_duo_fit_plot.png
:name: fig-duo-fit
:alt: Duo fit plot
:width: 100%

Verification of the VIS magnitude and F814W magnitude fits. Left: The x-axis is the measured VIS magnitude from Euclid and the y-axis is the predicted VIS magnitude from the LSST DP2 photometry. Right: The x-axis is the measured F814W magnitude from HST and the y-axis is the predicted F814W magnitude from the LSST DP2 photometry. The colorbar indicates the number of objects in each bin. The red line shows $x=y$.
```

{numref}`fig-duo-fit` shows that the magnitudes predicted from the LSST DP2 photometry reproduce the measured space-based magnitudes, with a median absolute deviation of about 0.2 mag for both VIS and F814W. For each object in the LSST DP2 dataset, we can therefore compute the blending entropy with Euclid as the reference, using the VIS magnitude predicted from its $griz$ photometry, or with HST, using the F814W magnitude predicted from its $i$-band photometry.



## Results

Integrated over all magnitudes, $16.7\%$ of the LSST–Euclid groups shown in {numref}`fig-nm-groups` contain more galaxies than LSST objects, i.e. contain unrecognized blends; this fraction is $40.8\%$ for the LSST–HST groups. Counted per object, $18.2\%$ of the 1,656,027 matched LSST objects are unrecognized blends with Euclid as the reference, and $46.8\%$ of the 22,326 with HST.

We now examine how blending depends on magnitude, and use the blending entropy to determine how ambiguous these blends are. To do so, we use the blending entropy computed for each LSST DP2 object. Objects with $S_\text{b} > 0$ overlap at least two galaxies and are therefore blends, while objects with $S_\text{b} = 0$ overlap a single galaxy. Among blends, we call *ambiguous blends* those with $S_\text{b} > 0.2$, i.e. whose galaxy association is ambiguous; see {cite:t}`Ramel26` for a detailed justification of this threshold. {numref}`fig-mag-highsb` shows the fractions of both populations as a function of LSST $i$-band magnitude.

```{figure} ./assets/plots/DR1_duo_plot_mag_highsb.png
:name: fig-mag-highsb
:alt: Fraction of blends and ambiguous blends as a function of i-band magnitude
:width: 100%

a) Distribution of detection magnitudes for LSST (blue), Euclid (orange) and HST (green) in ECDFS. Since the observation bands of these telescopes do not cover the same wavelength ranges, the Euclid VIS and HST F814W magnitudes are converted to the LSST $i$ band with a dedicated fit, used only for this panel and distinct from the fits described in the Methods section. b) Fraction of LSST DP2 objects with $S_\text{b} > 0$ (circles, blends) and $S_\text{b} > 0.2$ (squares, ambiguous blends), with either Euclid or HST as reference space-based data. The error bars are 68% Wilson binomial confidence intervals.
```

{numref}`Fig. %s-a) <fig-mag-highsb>` shows the magnitude distribution for each survey. The HST observations are much deeper than both LSST and Euclid.
{numref}`Fig. %s-b) <fig-mag-highsb>` shows the fraction of blends ($S_\text{b} > 0$) and the fraction of ambiguous blends ($S_\text{b} > 0.2$) as a function of magnitude. The fraction of blends is higher for HST than for Euclid, because HST has a better resolution and a greater depth. Many of the additional HST blends consist of a bright galaxy and a much fainter one that Euclid does not detect. For both reference surveys, the fraction of blends increases with magnitude, since fainter objects are more likely to be blended. This trend breaks down at $i \simeq 24$ with Euclid as the reference; we interpret this as a depth effect: for fainter LSST objects, the fainter galaxy of the blend increasingly falls below the Euclid detection limit. The fraction of blends exceeds $20\%$ for Euclid, which is consistent with the results reported by {cite:t}`SITCOMTN-128` and {cite:t}`Troxel23`.

After applying the $S_\text{b} > 0.2$ cut, the fractions of ambiguous blends obtained with the two reference surveys agree up to $i \simeq 24$, where $20\%$ of DP2 objects are ambiguous blends with either Euclid or HST as reference. The difference between the two $S_\text{b} > 0$ curves at brighter magnitudes therefore comes from faint galaxies detected by HST but not by Euclid: the corresponding blends are not ambiguous, since the LSST detection is unambiguously associated with the brighter galaxy of the blend. Perfect agreement between the two references is not expected: the fractions are computed over different footprints, and the HST footprint covers only 0.129 deg{sup}`2`, about 60 times less than the Euclid one, so that the HST fractions are subject to significant sample variance.

<!-- In summary, the fraction of unrecognized blends in DP2 depends strongly on the depth and resolution of the reference survey, from 16.7% with Euclid to 40.8% with HST, but most of this difference comes from faint companions that do not make the galaxy association ambiguous. The fraction of ambiguous blends is, in contrast, robust to the choice of reference survey down to the Euclid depth limit, with about one in five DP2 objects being an ambiguous blend at $i \simeq 24$. -->

## Discussion
In this technote, we matched LSST DP2 objects to Euclid DR1 and HST galaxies in the ECDFS with a FoF + EOT procedure and found that $16.7\%$ of the LSST–Euclid groups and $40.8\%$ of the LSST–HST groups contain more galaxies than LSST objects, i.e. contain unrecognized blends ($18.2\%$ and $46.8\%$ of matched objects). We used the blending entropy $S_\text{b}$ to show that the two reference surveys give comparable fractions of ambiguous blends down to $i \simeq 24$, where about one in five DP2 objects is an ambiguous blend.

We repeated the same analysis on DP1, whose PSF is smaller than that of DP2, and found a fraction of unrecognized blends that is broadly similar to the DP2 one. This suggests that the improvement in image quality alone may reduce the blend fractions less than naively expected, although DP1 and DP2 also differ in depth and footprint. A follow-up study will repeat this analysis as a function of image quality to quantify this dependence directly.

The blend fractions reported here apply to DP2 and are expected to decrease in later LSST data releases. The image quality in LSST DR1 is expected to be significantly better than in DP2, which reduces the overlap between neighboring sources and should therefore yield lower unrecognized blend fractions {cite}`Bosch18,Sanchez21`. This improvement may be partly offset by the greater depth of DR1, which will detect more faint galaxies, and therefore more faint companions within the footprints of LSST objects.
A follow-up study will repeat this analysis as a function of image quality to quantify directly how the blending fractions improve as the delivered image quality evolves.

These results matter most for weak lensing. Unrecognized blends bias the shapes measured by the pipeline, and this bias propagates to the shear estimates. DESC will calibrate it with image simulations, which must reproduce the blending found in real data {cite}`MacCrann22`; the fractions of unrecognized and ambiguous blends measured here as a function of magnitude provide a direct test of this realism. The matched catalogs go further, since they identify unrecognized blends individually: they can be used to evaluate the LSST deblender and its blending flags on real data. Beyond diagnosis, our comparison also points to a mitigation strategy. Because Euclid recovers as many ambiguous blends as HST down to $i \simeq 24$, joint processing of Rubin and Euclid data, as planned for the Rubin–Euclid Derived Data Products {cite}`Guy22`, could identify most of these blends over the large common footprint of the two surveys.


## Appendix

(appendix-fit-coeffs)=
### Coefficients of the magnitude fits

Euclid VIS fit:

- $a_0^{\text{low}} = 5.711$
- $a_0^{\text{high}} = 3.624$
- $c_r^{\text{low}} = 0.809$
- $c_r^{\text{high}} = 0.904$
- $c_{g-r} = 0.007$
- $c_{r-i} = -0.880$
- $c_{i-z} = -0.007$

HST F814W fit:

- $c_0 = 0.043$
- $c_i = 0.995$

## References

```{bibliography}
```


