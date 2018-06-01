import util
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

class FeatureExtractor:

    def __init__(self):
        print("Instantiating feature extractor...")
        self._train()


    def _train(self):

        # self.ohe_hour = OneHotEncoder(sparse=False)
        # self.ohe_hour.fit(np.array(range(0,48)))
        #
        # self.ohe_month = OneHotEncoder(sparse=False)
        # self.ohe_month.fit(np.array(range(0, 12)))
        #
        # self.ohe_day = OneHotEncoder(sparse=False)
        # self.ohe_day.fit(np.array(range(0, 31)))

        train_x = np.zeros(shape=[365 * 48, 3])

        for i in range (0, (365 * 48)):
            train_x[i][0] = i%48

        for i in range (0, (365 * 48)):
            train_x[i][1] = i%7

        for i in range (0, (365 * 48)):
            train_x[i][2] = i%12

        self.ohe = OneHotEncoder(sparse=False)
        self.ohe.fit(train_x)

    def get_features(self, state, action):
        '''
        Compute the features from the state to extract the q-value
        :param state:
        :param action:
        :return: a list of feature values
        '''

        time_feat = util.Counter()
        time_feat['hour'] = state.time.apply(lambda dt: ((dt.hour * 60) + dt.minute) // 30)
        time_feat['dayofweek'] = state.time.dt.dayofweek
        time_feat['month'] = state.time.dt.month - 1

        # Transform and avoid the dummy variable trap
        features = self.ohe.transform(np.array([time_feat['hour'], time_feat['dayofweek'], time_feat['month']])
                                      .reshape(1, -1))[:, :-1]

        features = list(features[0])

        features.append(state.energy_consumption)
        features.append(state.energy_generation)
        features.append(state.battery_curr)

        # TODO Embed action as a feature into this


        # Transforming into apt data structure
        feat_dict = util.Counter()
        for i in range(len(features)):
            feat_dict['f_'+str(i)] = features[i]

        return feat_dict
