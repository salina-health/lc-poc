# Laryngeal cancer triage proof-of-concept

This repository contains code to process voice recordings and train a RF model to classify recordings for triage onto the appropriate treatment pathway (cancer or not cancer).

The inputs to the model are features extracted from a 3 second sample of the audio, such as the mean pitch, shimmer and jitter.

The output from the model is a classification "C" (1) for cancer, or "N" (0) for non-cancer.

# Software environment

This is primarily a Python 3.8 project, with scripts and notebooks.

This code was run on an Intel Mac hardware, using [Miniconda](https://docs.anaconda.com/miniconda/) for the environment.

Set up the environment with:

```
conda env create -f environment.yaml
conda activate lc-poc
```

You will also need to install Surfboard, which provides WAV manipulation code and also implements algorithms for extracting features from the audio. We installed this from source: <https://github.com/novoic/surfboard>

We used [ffmpeg](https://ffmpeg.org) for audio conversion, and [Audacity](https://www.audacityteam.org) to view the audio.

# Data

We have 107 records of which 9 have a cancer diagnosis.

## Recordings

![Example waveform](img/illustrated-audio.png)

The recordings contained a number of activities, of which we only processed the "ah" extended vowel sound.

The audio recordings are not included in this repository. They are `.m4a` format collected on a Trust iPhone. In the code here you will see references to folders such as `secret/luhft/2023-03-27/Recordings`.

## Associated demographic and classification data

For each recording, a spreadsheet (`AI data.xlsx`, not included here) gives:

- Study Number (integer)
- Gender (Male or Female)
- Age (integer)
- Smoker (Current, Non, Ex)
- Diagnosis (various, e.g., Normal or Right vocal cord paralysis)
- Voice recording (blank - contained the embedded audio file)
- Classification (C or N for cancer or non-cancer)

We did not use the demographic fields in this work.

## Alternative data sets

Useful alternative data sources, which we used to help size the models before training on the laryngeal cancer data:

- [Mobile Device Voice Recordings at King's College London (MDVR-KCL) from both early and advanced Parkinson's disease patients and healthy controls](https://zenodo.org/records/2867216#.ZBgghxXP0UE)

- [Assessment of Speech Intelligibility in Parkinson’s Disease Using a Speech-To-Text System](https://ieeexplore.ieee.org/document/8070308)


# Pipeline

## 1. Convert to WAV

Audio files were converted to WAV files, with a consistent sampling rate of 48000. See [resample.sh](https://github.com/salina-health/lc-poc/blob/main/resample.sh) for the commands.

## 2. Isolation of "ah" sound

We listened to each recording in Audacity, and logged the time (in seconds) just before the "ah" sound started. We created a new file (`AI data.csv`) and appended on two columns to those listed above:

- Start ah (time in seconds just before "ah" sound)
- Observations (text noting anything unusual)

An example observation might be "S (subject) gave two sounds; we took the second one".

The script [ah.py](https://github.com/salina-health/lc-poc/blob/main/ah.py) was used to read the CSV file and write out three seconds of audio starting from the "ah" sound. For example, for the first row, "Study number 1", we look for 'Study 0001.wav' and write "ah Study 0001 3 sec.wav".

We re-listened to the "ah" extracted audio to manually check for quality.

## 3. Data exploration

See the notebook [summary.ipynb](https://github.com/salina-health/lc-poc/blob/main/summary.ipynb) for initial exploration of the data.

## 4. Feature extraction and training

See [explore-rf-3sec.ipynb](https://github.com/salina-health/lc-poc/blob/main/explore-rf-3sec.ipynb).

The notebook is made up of three main parts:

1. Feature extracting, using Surfboard. This writes a file called `AI data with features 3 seconds.csv` which contains the classification data, study number, and then audio features. 

2. Training. We used 5-fold cross validation training with stratified split on the data (so each fold had some amount of positive data in it). We excluded columns will NaN/missing data for a feature.

    As the data is unbalanced, we used the `class_weights` feature of the RandomForestClassifier code to adjust for this.

3. Reporting. The last part of the notebook investigates the feature importance,  training on all data to see the effect.


## 5. Observations

The F1 metric was not as informative as we hoped. The problem here is capture all the true positives at the expense of false negatives. 


## 6. Next steps

- More data

- Consider F2 or alternative scoring. References here are: [Unbalanced breast cancer data classification using novel fitness functions in genetic programming](https://www.sciencedirect.com/science/article/abs/pii/S0957417419305767?via%3Dihub) via [Loss Functions and Metrics in Deep Learning](https://arxiv.org/abs/2307.02694).

- Transfer learning: consider using [HeaR](https://github.com/Google-Health/google-health/blob/master/health_acoustic_representations/README.md) to compute an embedding for the audio, and train this downstream task on that representation. Google have approved us for access to HeaR for this application.

# Related work



# How to cite this work

Dallaway, R., Goonatilake, S. (2023). Laryngeal cancer triage proof of concept. https://github.com/salina-health/lc-poc


```
@misc{lcpoc,
  author       = {Dallaway, R. and Goonatilake, S.},
  title        = {Laryngeal cancer triage proof of concept},
  year         = {2023},
  url          = {https://github.com/salina-health/lc-poc},
}
```

This project is co-funded by Salina Health Ltd and [Innovate UK](https://www.ukri.org/councils/innovate-uk/), the UK’s innovation agency.

![Innovate UK](img/innovate-uk-small.jpg)






    	
   






