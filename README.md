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

Final training set: 
![Alt text](https://github.com/michaelmoschitto/AISongRecommender/blob/main/Data/Visualizations/TrainingData.png?raw=true "Title")

## Model
The Model is a Keras sequential classifier with 10 input features and 4 outputs (Happy, Sad, Calm, Energetic). It features
two dense layers with relu and softmax activation functions and the Adam optimizer. When classifying all 4 moods the model ranged from 
~74-76 % accuracy and an F1-Score of ~73%. We found this reasonable as the feeling that one song elicits is often subjective with 
only slight variation between Calm/Sad and Happy/Energetic. When predicting opposites such as Energetic/Sad it was much higher in with
accuracies in the mid 90's. 

   
## Results 
Despite the accuracy not being in the 80's or 90's, we were able to achieve great results. 
We were able to produce data frames of songs labeled with moods as seen below.

![Alt text](https://github.com/michaelmoschitto/AISongRecommender/blob/main/Data/Visualizations/Results.png?raw=true "Title")

## Listen to the Results!
The best way to validate our results is to actually listen to the playlists created. They can be found on mikeydays Spotify account and are linked below!

Calm: https://open.spotify.com/playlist/2D95LpUtwJqVYN1NG4rM8S

Energetic: https://open.spotify.com/playlist/37XoFkuajvPUsLZfidsFAP

Happy: https://open.spotify.com/playlist/5FsxoaKvSUZyl9noSlYlwx

Sad: https://open.spotify.com/playlist/4J6O4ytzIfPzjCIgToiEkY

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


