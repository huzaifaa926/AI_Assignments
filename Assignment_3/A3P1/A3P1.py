import os
import pandas as pd
from math import exp, pi, sqrt
import pickle
# pd.set_option("display.precision", 16)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_SET_DIR = os.path.join(BASE_DIR, 'DataSets')
PICKLE_DIR = os.path.join(BASE_DIR, 'Pickles')
PICKLE_DATA = os.path.join(PICKLE_DIR, 'GaussianNaiveBayesClassifierModel.pickle')
TRAINING_DATA = os.path.join(DATA_SET_DIR, 'parktraining.xlsx')
TESTING_DATA = os.path.join(DATA_SET_DIR, 'parktesting.xlsx')

class GaussianNaiveBayesClassifier():
    
    def __init__(self, training_data, training_labels, testing_data, testing_labels):
        self.__training_data = training_data
        self.__training_labels = training_labels
        self.__testing_data = testing_data
        self.__testing_labels = testing_labels
        self.__no_of_classes, self.__classes = self.__extract_classes()
        self.__scaling_func = "min-max-scaling"     # Default scaling function
        self.__classes_probabilities = {x: 0 for x in self.__classes}
        self.__prior_probability()

        # Some utility varibles
        self.__training_data_scaled = None
        self.__training_data_mean = None
        self.__training_data_variance = None

    def __feature_scaling(self, scaling_func=None, train=True):
        
        if scaling_func is not None:
            self.__scaling_func = scaling_func
        else:
            scaling_func = self.__scaling_func

        if scaling_func == "min-max-scaling":
            if train:
                self.__training_data_scaled = min_max_scaling(self.__training_data)
            else:
                return min_max_scaling(self.__testing_data)

        elif scaling_func == "mean-normalization":
            if train:
                self.__training_data_scaled = mean_normalization(self.__training_data)
            else:
                return mean_normalization(self.__testing_data)

        elif scaling_func == "z-score-normalization":
            if train:
                self.__training_data_scaled = z_score_normalization(self.__training_data)
            else:
                return z_score_normalization(self.__testing_data)

        elif scaling_func == "False":
            if train:
                self.__training_data_scaled = self.__training_data
            else:
                return self.__testing_data
        else:
            raise Exception("Not a Valid Scaling Function!")

    def __extract_classes(self):
        if len(self.__training_labels.unique()) != len(self.__testing_labels.unique()):
            raise Exception("Size Of (Distinct) Training Labels And Tesing Labels Are Not Same")
        return len(self.__testing_labels.unique()), self.__testing_labels.unique()

    def __prior_probability(self):
        total = len(self.__training_labels)
        for _class in self.__classes:
            self.__classes_probabilities[_class] = self.__training_labels.value_counts()[_class] / total

    def train(self, scaling_func=None):

        if scaling_func is not None:
            self.__scaling_func = scaling_func
        else:
            scaling_func = self.__scaling_func
            
        self.__feature_scaling(scaling_func)
        # Concatinating with labels
        training_data_concat_labels = self.__training_data_scaled.join(self.__training_labels)
        # Mean and Variance, group by labels
        self.__training_data_mean  = training_data_concat_labels.groupby(training_data_concat_labels.columns[-1]).mean()
        self.__training_data_variance =  training_data_concat_labels.groupby(training_data_concat_labels.columns[-1]).var()

        # print(self.__training_data_mean)
        # print(self.__training_data_variance)

    def predict(self, verbose=False):

        scaling_func = self.__scaling_func

        testing_data_scaled = self.__feature_scaling(scaling_func, train=False)        
        predicted = []

        for row in range(len(testing_data_scaled)):
            predicted.append(self.__baysian_probability(testing_data_scaled.loc[row]))

        accuracy = self.__calculate_accuracy(predicted, verbose)
        print("Accuracy: ", accuracy*100)
        

    def __calculate_accuracy(self, predicted, verbose=False):
        correct_count = 0
        for i,j in zip(self.__testing_labels, predicted):
                # print(f"Actual: {i}\tPredicted: {j}")
            if i==j:
                if verbose:
                    prGreen(f"Actual: {i}\tPredicted: {j}")
                correct_count+=1
            else:
                if verbose:
                    prRed(f"Actual: {i}\tPredicted: {j}")

        return correct_count/len(self.__testing_labels)

    def __baysian_probability(self, features):
        # x_ = e ^ -((x-mean)^2 / 2 * variance) / sqrt(2 * pi * variance)
        prob_by_classes = {}
        multiplied_prob = 1
        normalized_prob_factor = 0
                
        for _class in self.__classes:
            prob = []
            multiplied_prob = 1
            for feature in range(len(features)):
                try:
                    prob.append( \
                        exp(-((features[feature]-self.__training_data_mean[feature][_class])**2 / (2 * self.__training_data_variance[feature][_class]))) \
                        / sqrt(2 * pi * self.__training_data_variance[feature][_class])
                    )
                except ZeroDivisionError:
                    prob.append(1e-100)
            for p in prob:
                multiplied_prob = multiplied_prob * p

            prob_by_classes[_class] = multiplied_prob * self.__classes_probabilities[_class]
            normalized_prob_factor += prob_by_classes[_class]
        
        for _class in self.__classes:
            prob_by_classes[_class] = prob_by_classes[_class] / normalized_prob_factor

        key_max = max(prob_by_classes.keys(), key=(lambda k: prob_by_classes[k]))
        # print(prob_by_classes[key_max], key_max)
        # print(prob_by_classes, prob_by_classes[0]+prob_by_classes[1])
        return key_max



    def summary(self):
        print("*"*35)
        print("\tMODEL SUMMARY\n")
        print("Number of classes/labels: ", self.__no_of_classes)
        print("\nPrior Probabilites")
        for _class in self.__classes:
            print(f"Class#{_class}: {self.__classes_probabilities[_class]}")
        print()
        print("Feature Scaling Function: ", self.__scaling_func)
        print()
        print("Number of trainable columns: ", len(self.__training_data.columns))
        print("Number of trainable rows: ", len(self.__training_data))
        print()
        print("Number of testing columns: ", len(self.__testing_data.columns))
        print("Number of testing rows: ", len(self.__testing_data))
        print()
        print("*"*35)

def calculate_mean(data_frame):
    return data_frame.mean()

def calculate_variance(data_frame):
    return data_frame.var()

def min_max_scaling(data_frame):
    # Extracting column names
    columns = data_frame.columns.tolist()
    data_frame_scaled = []
    for column in columns:
        temp = []
        max_element = max(data_frame[column])
        min_element = min(data_frame[column])
        for x in data_frame[column]:
            _x = (x - min_element) / (max_element - min_element)
            temp.append(_x)
        data_frame_scaled.append(temp)
    
    #Transposing it, because above, columns are appended as a row
    return pd.DataFrame(data_frame_scaled).T

def mean_normalization(data_frame):
    # Extracting column names
    columns = data_frame.columns.tolist()
    data_frame_mean = calculate_mean(data_frame)
    data_frame_scaled = []
    for column in columns:
        temp = []
        max_element = max(data_frame[column])
        min_element = min(data_frame[column])
        for x in data_frame[column]:
            _x = (x - data_frame_mean[column]) / (max_element - min_element)
            temp.append(_x)
        data_frame_scaled.append(temp)
    
    #Transposing it, because above, columns are appended as a row
    return pd.DataFrame(data_frame_scaled).T

def z_score_normalization(data_frame):
    # Extracting column names
    columns = data_frame.columns.tolist()
    data_frame_mean = calculate_mean(data_frame)
    data_frame_std = calculate_variance(data_frame).apply(lambda x: x**0.5)
    data_frame_scaled = []
    for column in columns:
        temp = []
        for x in data_frame[column]:
            _x = (x - data_frame_mean[column]) / (data_frame_std[column])
            temp.append(_x)
        data_frame_scaled.append(temp)
    
    #Transposing it, because above, columns are appended as a row
    return pd.DataFrame(data_frame_scaled).T

if __name__ == "__main__":
    try:
        pickle_input = open(PICKLE_DATA, "rb")
        model = pickle.load(pickle_input)
        pickle_input.close()
        model.summary()
        model.predict(verbose=True)

    except FileNotFoundError:
        # Loading training data
        train_df = pd.read_excel(TRAINING_DATA, header=None)
        # Separating training labels
        training_labels = train_df.pop(train_df.columns[-1])
        training_data = train_df
        
        # Loading testing data
        test_df = pd.read_excel(TESTING_DATA, header=None)
        # Separating testing labels
        testing_labels = test_df.pop(test_df.columns[-1])
        testing_data = test_df

        # print(training_data.head(), training_labels.head())
        # print(training_data.tail(), training_labels.tail())

        # print(testing_data.head(), testing_labels.head())
        # print(testing_data.tail(), testing_labels.tail())

        model = GaussianNaiveBayesClassifier(training_data, training_labels, \
                                                testing_data, testing_labels)
        model.train()
        pickle_output = open(PICKLE_DATA, "wb")
        pickle.dump(model, pickle_output)
        pickle_output.close()
        model.summary()
        model.predict(verbose=True)