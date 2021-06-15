# AISongRecommender
A neural net that uses mood and genre to recommend the perfect song.



## Libraries

```python
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score, KFold

```

## Environment

This project uses a virtual Python environment (venv) to control which packages 
have been downloaded and standardize across multiple machines.

To activate Unix/Linux: <br>
    * ```cd /AISongRecommender ```<br>
    * ``` source AISongRec/bin/activate ```

To activate windows: <br>
* ```cd \ AISongRecommender ```<br>
* ``` .\powershellEnv\Scripts\```

## Data Collection
With limited datasets available, a large part of this project was creating our own training and testing sets. This was done
using the Spotify Web API and wrapper library Spotipy. Our model was trained on a dataset aggregated from mood labeled playlists 
created by various Spotify users. The testing set is an aggregation of songs from multiple playlists from Michael's account.

All data engineering related code can be found in the SpotifyWrapper.py file.

## Model
The Model is a Keras sequential classifier with 10 input features and 4 outputs (Happy, Sad, Calm, Energetic). It features
two dense layers with relu and softmax activation functions and the Adam optimizer. When classifying all 4 moods the model ranged from 
~74-76 % accuracy and an F1-Score of ~73%. We found this reasonable as the feeling that one song elicits is often subjective with 
only slight variation between Calm/Sad and Happy/Energetic. When predicting opposites such as Energetic/Sad it was much higher in with
accuracies in the mid 90's. 

   ### Features
   Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo,        rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.

   Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
   
   Instrumentalness: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
   
   Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides a strong likelihood that the track is live.
   
   Loudness: the overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing the relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
   
   Speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audiobook, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
   
   Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
   Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, the tempo is the speed or pace of a given piece and derives directly from the average beat duration.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


