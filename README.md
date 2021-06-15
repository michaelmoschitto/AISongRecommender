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
import face_recognition

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

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


