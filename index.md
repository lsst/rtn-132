# Unrecognized blends in LSST DP1 and DP2 from the comparison with Euclid and HST

See the [Documenteer documentation](https://documenteer.lsst.io/technotes/index.html) for tips on how to write and configure your new technote.

```{abstract}
Unrecognized blends, where the number of detected objects is smaller than the number of true sources, are a known issue in LSST data and a significant source of photometric error. In this technote, we present our methodology for identifying unrecognized blends in the LSST Data Preview 1 and Data Preview 2 (hereafter DP1 and DP2, respectively) datasets by comparing them with high-resolution space-based observations from the Euclid Q1 and Hubble Space Telescope (HST) in the Extended Chandra Deep Field South (ECDFS). By matching sources detected in the LSST data with those from the space telescopes, we quantify the fraction of sources that are blended in LSST but resolved in the space-based data. We find that up to 22% of sources in both DP1 and DP2 are unrecognized blends when compared to Euclid Q1 data at 23 < i-band magnitude < 24. When compared to HST data, the fraction of unrecognized blends reaches up to 40% for the same magnitude range. We finally use the blending entropy to quantify, for each of those unrecognized blends in the LSST data, how ambiguous its galaxy association is.
```

## Data
<!-- ECDFS | LSST DP1 and DP2 (what changes between the two) | Euclid Q1 | HST -->
<!-- The Extended Chandra Deep Field South (ECDFS) is a deep-sky survey field that has been observed by multiples telescopes at different wavelengths due to its low galactic obscuration {cite}`Lehmer05`. The LSST Data Preview 1 (DP1) {cite}`RTN-095` and Data Preview 2 (DP2) {cite}`RTN-115` both cover the ECDFS field.

The LSST DP datasets both have a pixel scale of 0.2 arcsec/pixel while the Euclid Q1 data has a pixel scale of 0.1 arcsec/pixel and HST has a pixel scale of 0.05 arcsec/pixel. -->


Blending, where multiple sources overlap in the sky, is expected to be a significant source of measurement uncertainties in the Stage-IV surveys like LSST {cite}`Melchior21`. A way to study blending is to compare data from different telescopes with different resolutions and depths.

The Extended Chandra Deep Field South (ECDFS) is a deep-sky survey field that has been observed by many telescopes at different wavelengths due to its low galactic obscuration {cite}`Lehmer05`. In this note we use imaging of the ECDFS from three facilities.

- **Rubin LSST:** Rubin Observatory's Data Previews are early releases that precede LSST Data Release 1. Data Preview 1 (DP1) {cite}`RTN-095` is based on commissioning observations from the LSST Commissioning Camera (LSSTCam's smaller predecessor, ComCam) and includes ECDFS among its fields. Data Preview 2 (DP2) {cite}`RTN-115` is the first preview based entirely on data from the full LSST Science Camera (LSSTCam) and also covers the ECDFS. Both have a pixel scale of 0.2 arcsec/pixel. To access the LSST DP2 data, we use the Rubin Science Platform (RSP) and the `butler` API to access the data. The following parameters are used to specify the repository, collection, skymap, and catalog:

```python
repo='dp2_prep'
collection = 'LSSTCam/runs/DRP/DP2/v30_0_8/DM-55060/stage3'
skymap = 'lsst_cells_v2'
butler_cat = 'object'
```
- **Euclid Q1:** The Euclid Quick Data Release 1 (Q1) {cite}`EuclidQ1` is an early release of Euclid imaging and spectroscopy over ~63 deg² in the three Euclid Deep Fields, one of which is the ECDFS. We use the VIS optical imaging which has a pixel scale of 0.1 arcsec/pixel.  We use the final MER (MERge) catalog from Euclid Q1, which merges the VIS and NISP space-based imaging with external ground-based data to produce the combined multi-band source catalog.
- **HST:** The Hubble Space Telescope has also imaged the ECDFS {cite}`HSTref`, we use these data as high-resolution imaging with a pixel scale of 0.06 arcsec/pixel. We use the Hubble Legacy Fields (HLF) GOODS-South source catalog, which is a high-level science product derived from archival HST imaging.


<!-- `LSSTCam/runs/DRP/DP2/v30_0_8/DM-55060/stage3` -->

<!-- For LSST DP, point-like sources are removed with `i_extendedness == 1`. -->

```{figure} ./assets/plots/ecdfs_two_panel_vertical.png
:name: fig-ecdfs
:alt: ECDFS
:width: 100%

Top: One tenth of the detected galaxies in the ECDFS observed by LSST. The blue region corresponds to our region of study we chose this region to not have the single visits effects (lower magnitude detections and artifacts). The grey region is discarded due to the presence of single visits. The circle discrimnating the two regions has a radius on the sky of  2.1 degrees and centered around the coordinates RA=53.05, Dec=-28.15 degrees.
Bottom: One tenth of the detected galaxies in the ECDFS observed by LSST, Euclid and HST.
```

The Euclid ECDFS footprint has an area of ~15.53 deg$^2$ and contains a total of 5,328,489 galaxies detected in the VIS band and, in that same footprint, there are 2,416,305 objects detected in the LSST DP2 dataset.\
The HST ECDFS footprint has of area 0.18 deg$^2$ and contains a total of 165,776 galaxies detected in the F814W band and, in that same footprint, there are 33,240 objects detected in the LSST DP2 dataset.

In the following sections, we will refer as `objects` the sources detected in the LSST DP datasets and as `galaxies` the sources detected in the Euclid and HST datasets. We will also refer to `blends` as the objects that are associated with more than one galaxy. Moreover, the plots shown, unless stated otherwise, are for the LSST DP2 dataset. The results for the LSST DP1 dataset are similar and can be found in the Appendix of this technote.

## Methods

### Matching LSST DP catalogs with Euclid and HST

We match the sources detected in the LSST DP datasets with those from Euclid and HST using a two-step process:

1. Friends-Of-Friends (FoF) catalog matching {cite}`FoFMatching`: Iteratively and transitively connecting "friends" pairs within a specified linking length and merging their associated groups. It starts with each object as its own group, then recursively merges groups if any member of one group is within the linking length of any member of another. The choice of linking length defines the scale of the resulting structures. We chose a linking length of 2 arcsec to make coarse groups.
2. Ellipse Overlap Test (EOT): For each element (object/galaxy) in each group, we check if the ellipses (computed from the semi-major and semi-minor axes and the position angle of the detection) of the elements overlap with the ellipses of the other elements. If they do, we consider them as matched and keep them as a group. If there is no overlap, we split the group into two subgroups and repeat the process until all elements in each group have overlapping ellipses.

Adding the EOT step after the FoF matching makes our matching independant from the linking length choice. The result of this matching is a set of groups where each groups contains one or more objects and one or more galaxies. If multiple elements are in the group, then they are overlapping, at least transitively.
After making this matching, we can compute the number of objects and galaxies per group, as shown in {numref}`fig-nm-groups`.

```{figure} ./assets/plots/detect_counts_cbar_on_bottom_vertical.png
:name: fig-nm-groups
:alt: N-M groups
:width: 90%

Result of the cross-matching of catalogs LSST-Euclid and LSST-HST using FoF+EOT matching method. Each bin in the 2D histogram represents a group for a given number of objects, meaning LSST detections in columns and galaxies, meaning Euclid detections (top) or HST detections (bottom) in rows. The colorbar indicates the number count of groups in each bin.
```

We call unrecognized blends the groups having more galaxies than objects which corresponds to the lower left part of {numref}`fig-nm-groups`. The fraction of unrecognized blends is higher for HST is higher than Euclid due to the higher resolution and depth of the HST data. Using this plot, we estimate that 13.8% of LSST DP2 objects are unrecognized blends when compared to Euclid and 38.7% when compared to HST.

### Blending entropy

For each object detected in the LSST DP, we can assign it a blendy entropy score {cite}`Ramel26` which quantifies how ambiguous its galaxy association is. The blending entropy for a given wavelength band is defined as:

```{math}
S_\text{b} = -\sum_{\text{g}\in\text{gal}} p_\text{og} \ln(p_\text{og}) \ge 0 \quad \text{with} \quad p_\text{og} \propto \left\langle \text{o},\text{g} \right\rangle \exp\left(-\left|  m_\text{o}-m_\text{g}\right|\right)
```

$p_\text{og}$ is the matching probability of object `o` with a galaxy `g`. It is the intersection-over-union of the two ellipses: the area they share divided by the area they cover together from 0 (disjoint) to 1 (identical). It is also normalized per object so that $\sum_{\text{g}\in\text{gal}}p_\text{og} = 1$. Systems with one object and one galaxy have a matching probability of 1 and a blending entropy of 0. The blending entropy ranges from 0, meaning no ambiguity, to log(N), meaning maximum ambiguity with N being the number of galaxies in the group.

```{figure} ./assets/high_blending_entropy.png
:name: fig-high-sb-image
:alt: High Sb

Example of a high $S_\text{b}$ blend. Top: LSST cutout with $i,r,g$ bands corresponding to red, green and blue respectively. Bottom: Euclid VIS. The object from the LSST detection is represented by the blue ellipse and the galaxies from the Euclid detections by the orange ellipses.
```

{numref}`fig-high-sb-image` shows an example of a high blending entropy system with one object and two galaxies. The object overlaps with both galaxies and has a similar magnitude to both of them, making it ambiguous to which galaxy it is associated.
The blending entropy for this system is $S_b = 0.69$.

```{figure} ./assets/low_blending_entropy.png
:name: fig-low-sb-image
:alt: Low Sb

Example of a low $S_\text{b}$ blend.Top: LSST cutout with $i,r,g$ bands corresponding to red, green and blue respectively. Bottom: Euclid VIS. The object from the LSST detection is represented by the blue ellipse and the galaxies from the Euclid detections by the orange ellipses.
```

Conversely, {numref}`fig-low-sb-image` shows an example of a low blending entropy system with one object and two galaxies. One of the Euclid detections overlaps almost entirely with the LSST detection, while the other is only partially overlapping and has a lower magnitude. The LSST detection is well associated with the first Euclid detection making it unambiguous to which galaxy it is associated.
The blending entropy for this system is $S_b = 0.09$.

**those are dp1 image, make dp2 images and vertical**

The blending entropy needs to computed for the same wavelength band. Since the LSST DP datasets have been obserbed in the $u g r i z y$ bands, we compute the blending entropy using the relevant amount of bands that are the closest to the Euclid VIS band and the HST F814W band and making a fit to be able to compare them. We chose to construct a fit on the following bands $gri$ and VIS for the LSST-Euclid comparison and $i$ and F814W for the LSST-HST comparison. The fit will be computed using solely the 1-1 systems since their photometry is cleaner than multiple-to-one systems and then applied to every object in the LSST DP datasets.

For Euclid, we use the following fit on the colors defined as:

$$
\mathrm{VIS}_{\mathrm{fit}} = r_{\mathrm{term}} + c_{g-r} \cdot (g - r) + c_{r-i} \cdot (r - i) + c_{i-z} \cdot (i - z)
$$

We decided to define $r_{\mathrm{term}}$ as a piecewise linear function of $r$:

- If $ r \leq 22 $:
  $r_{\mathrm{term}} = a_0^{\mathrm{low}} + c_r^{\mathrm{low}} \cdot r$

- If $ r > 22 $: $\,r_{\mathrm{term}} = a_0^{\mathrm{high}} + c_r^{\mathrm{high}} \cdot r$
  where we define $a_0^{\mathrm{high}} = a_0^{\mathrm{low}} + (c_r^{\mathrm{low}} - c_r^{\mathrm{high}}) \cdot 22$ to ensure continuity at $r = 22$.

The fitted coefficients are:

- $ a_0^{\text{low}} = 5.66629780 $
- $ a_0^{\text{high}} = 3.97249087 $
- $c_r^{\mathrm{low}} = 0.814976209$
- $c_r^{\mathrm{high}} = 0.891967433$
- $c_{g-r} = 0.00516430123$
- $c_{r-i} = -0.873242388$
- $c_{i-z} = -0.00569483576$

```{figure} ./assets/plots/visfit_vs_vis.png
:name: fig-visfit
:alt: VIS fit vs VIS
:width: 100%

Verification of the VIS fit. The x-axis is the measured VIS magnitude from Euclid and the y-axis is the predicted VIS magnitude from the LSST DP2 photometry. The colorbar indicates the number count of objects in each bin. The red line is the $x=y$ line.
```

For HST, we use the following fit on the $i$-band defined as:
$\mathrm{F814W}_{\mathrm{pred}} = c_0 + c_{i} \cdot i$

The fitted coefficients are:
- $ c_0 = -1.249 $
- $ c_i = 1.005 $

```{figure} ./assets/plots/f814wfit_vs_f814w.png
:name: fig-hstfit
:alt: F814W fit vs F814W
:width: 100%

Verification of the F814W fit. The x-axis is the measured F814W magnitude from HST and the y-axis is the predicted F814W magnitude from the LSST DP2 photometry. The colorbar indicates the number count of objects in each bin. The red line is the $x=y$ line.
```

{numref}`fig-visfit` and {numref}`fig-hstfit` show that the fits are <span style="color: red;"> good enough </span> to be used for the blending entropy computation.
We can then compute the blending entropy for each object in the LSST DP datasets for either Euclid, using the VIS fit from the $riz$ bands or HST, using the F814W fit from the $i$ band.


## Results

```{figure} ./assets/plots/unrec_frac_and_mag.png
:name: fig-unrec-frac
:alt: Fraction of unrecognized blends as a function i-band magnitude
:width: 100%

Top: Distribution of detection magnitudes for LSST (blue), Euclid (orange) and HST (green) in ECDFS. Since the observation bands of these telescopes do not cover the same wavelength ranges, a fit was made to compare them consistently using the LSST i-band as a reference. Bottom: Fraction of unrecognized blends as a function of magnitude in LSST DP2 with either Euclid or HST as the ground truth.
```

{numref}`fig-unrec-frac` shows that the HST observations are much deeper than those of the LSST and Euclid surveys. This explains the higher fraction of unrecognized blends for all magnitudes for HST: in these cases, objects detected as a single object by LSST are actually composed of one very bright object and another that is much fainter which HST detects but Euclid does not hence the discrepancy.
<!-- We can therefore assume that blends with HST as the ground truth are less problematic than those with Euclid, since the secondary object of is significantly less luminous. -->


```{figure} ./assets/plots/dp2_high_sb_unrec.png
:name: fig-high-sb-unrec
:alt: Fraction of high Sb blends as a function of i-band magnitude
:width: 100%

Fraction of high $S_b$ blends as a function of the i-band magnitude of LSST. The "$S_b$ all" values are the same as {numref}`fig-unrec-frac` since no cut has been made.
```


## References

```{bibliography}
```


