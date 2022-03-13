---
layout: post
title: External Links in NWB and DANDI
author: Saksham Sharda, CatalystNeuro
---

## External Files in NWB
External Files: video/audio files that are part of the experiment but are not stored in NWB as HDF5 format. 

## The need for external files
Neurophysiology experiments often include natural videos (such as behaving animals), which need to be stored with the neurophysiological recordings in order to ensure maximal reusability of the data. These videos are commonly stored with lossy compression (e.g. h264 in an .mp4 file), which allows them to achieve very high compression ratios. It is possible to read these videos frame-by-frame, and store them in HDF5, but since HDF5 is not able to access popular video codecs like h264, the volume of the video in the NWB file is much larger (even when using the available compression algorithms like GZIP). NWB has an option to avoid storing these altogether by linking to these external video files using a relative path to that file on disk. This relative path is stored in the ImageSeries neurodata_type storing it as an attribute of a string dtype. We also need to publish these video linked NWB files in an archive (e.g. in DANDI). For DANDI, which renames and reorganizes the the NWB files, this requires not only uploading the video file on the archive but also changing the path attribute of the ImageSeries to reflect the new file names. 

To implement this, we have created a formal naming convention for these video files relative to the NWB files' path. In addition, these video files are also placed in a specific folder structure relative to the new location of the NWB file during the `dandi organize` call.  

Internally the steps are as follows:

2. Organizing and renaming the video files with one of move/copy/symlink/hardlink in the new folder structure.
3. Updating the value of the `external_file` attribute in the NWB files. 
4. Uploading on DANDI. 

__Note__: this solution is specifically for natural videos like those of behaving animals. There are other types of image sequences like image stacks from optical physiology, which do not use codecs like h264; these types of videos can be copied into an HDF5 file.


## Example re-organization

### Original folder organization

```
├── nwbfiles
│   ├── test1_0_0.nwb
│   └── test1_1_1.nwb
└── video_files
    ├── test1_0.avi
    ├── test1_1.avi
    ├── test2_0.avi
    └── test2_1.avi
```
With the path attribute as: `image_series.external_files=["../video_files/test1_0.avi", "../video_files/test1_1.avi"]`

### After `dandi organize`
The renaming pattern is as follows `/<nwbfile_name>/{ImageSeries UUID}_external_file_{number}.mp4`.
This UUID is that assigned to the `ImageSeries` datatype when its created. Thus its possible to lookup a video file linked to an NWB file and vice versa. 

```
└── dandi_organized
    ├── sub-mouse0
    │   ├── sub-mouse0_ses-sessionid0_image
    │   │   ├── 933f8cf6-9e4b-405f-8cad-cc031d1fafc9_external_file_0.avi
    │   │   └── 933f8cf6-9e4b-405f-8cad-cc031d1fafc9_external_file_1.avi
    │   └── sub-mouse0_ses-sessionid0_image.nwb
    └── sub-mouse1
        ├── sub-mouse1_ses-sessionid1_image
        │   ├── 03137112-9d42-46b6-9046-45bc9aa7eb5e_external_file_0.avi
        │   └── 03137112-9d42-46b6-9046-45bc9aa7eb5e_external_file_1.avi
        └── sub-mouse1_ses-sessionid1_image.nwb
```
With the renamed path attribute as 

```
image_series.external_files=
["sub-mouse0_ses-sessionid0_image/933f8cf6-9e4b-405f-8cad-cc031d1fafc9_external_file_0.avi",
"sub-mouse0_ses-sessionid0_image/933f8cf6-9e4b-405f-8cad-cc031d1fafc9_external_file_1.avi"]
```

## Code Walkthrough

- __Register__ dataset on DANDI (staging)

```
cd dandi_organized
dandi download "https://gui-staging.dandiarchive.org/#/dandiset/101391/draft"
```

- __Organize__

```
cd dandi_organized
dandi organize -f "copy" --update-external-file-paths --media-files-mode "copy" "/nwbfiles"
```
__--modify-external-file-fields__ option is a flag.

If active, the organise operation modifies the `external_file` field of an `ImageSeries` that holds the local location of an associated video file. It changes the value to the new name as per the convention above.
If no `external_file` field found in all nwb files, but this option is active, then it logs a warning.
If any NWB file's `ImageSeries` has a `external_file`, but this option is not specified, then it raises a `ValueError` to avoid breaking the link.

__--media-files-mode__ can be any of copy/move/symlink/hardlink.

This can only be specified if the --modify-external-file-fields flag is True.
This is an optional argument, if not specified it defaults to "symlink": an efficient way to deal with possibly large video files.

- __Validate__

```
dandi validate
```

- __Upload__

```
dandi upload -i dandi-staging "/dandi_organized"
```

Example dandiset [here](https://gui-staging.dandiarchive.org/#/dandiset/100953/draft/files?location=)

- __download__

This dataset can then be downloaded using:
```
mkdir dandi_download
cd dandi_download
dandi download "https://gui-staging.dandiarchive.org/#/dandiset/101391/draft"
```
The folder will contain all the video files along with the dandi metadata .yml and .nwb files.
