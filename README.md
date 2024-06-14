# ChimpBehave

## Examples - walking, sitting, standing, running, hanging, climbing down, climbing up
<img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/walking.gif" width="140" height="140"><img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/sitting.gif" width="140" height="140"><img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/standing.gif" width="140" height="140"><img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/running.gif" width="140" height="140"><img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/hanging.gif" width="140" height="140"><img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/climbing_down.gif" width="140" height="140"><img src="https://github.com/MitchFuchs/ChimpBehave/blob/main/assets/gifs/climbing_up.gif" width="140" height="140">


## Data preparation
Download the ChimpBehave dataset found here: [url]

Save it in the data folder to match the following structure:

    ├── ...
    ├── data                                            # data folder
    │   ├── chimpbehave                                 # chimpbehave dataset folder 
    |   │   ├── bboxes                                  # bboxes annotations
    |   │   |   ├── Benga1_364_778_bboxes.json          # training image (name irrelevant) 
    |   │   |   ├── Benga1_843_1082_bboxes.json         # training image (name irrelevant) 
    |   │   |   ├── Benga1_1189_1371_bboxes.json        # training image (name irrelevant)
    │   |   |   └── ...                                 # etc.
    |   │   ├── miniclips                               # miniclips used in experiments
    │   |   |   └── ...                                 # this folder will be filled after the miniclip extraction (see instructions below)
    |   │   ├── original                                # original video sequences
    |   │   |   ├── Benga1_364_778.mp4                  # validation image (name irrelevant) 
    |   │   |   ├── Benga1_843_1082.mp4                 # validation image (name irrelevant) 
    |   │   |   ├── Benga1_1189_1371.mp4                # validation image (name irrelevant)
    │   |   |   └── ...                                 # etc.
    |   │   └──  labels.csv                             # file containing the behavior class label and id for each original sequence
    │   └── ...                   
    └── ...


## Extract miniclips for experiments
To extract miniclips from ChimpBehave, run the following commands: 

```
cd tools
python ./chimpbehave_extract_miniclips.py
```

## Using symlink (optional)
Note that if your dataset is stored in another location, you can use symlinks instead of duplicating it. 

```
ln -s /path/to/chimpbehave/original/*.mp4 /home/<user>/ChimpBehave/
```

## Reference

If you use this material, please cite it as below.

Fuchs, M., Genty, E., Bangerter, A., Zuberbühler, K., & Cotofrei, P. (2024). From Forest to Zoo: Great Ape Behavior Recognition with ChimpBehave. arXiv preprint arXiv:2405.20025.

```BibTeX
@misc{fuchs2024chimpbehave,
      title={From Forest to Zoo: Great Ape Behavior Recognition with ChimpBehave}, 
      author={Michael Fuchs and Emilie Genty and Adrian Bangerter and Klaus Zuberbühler and Paul Cotofrei},
      year={2024},
      eprint={2405.20025},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
