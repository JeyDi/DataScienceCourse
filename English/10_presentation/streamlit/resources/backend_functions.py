import pandas as pd
from pickle import load
import re
import os
import onnxruntime as rt
import numpy

from resources.path_dataset import get_folder_path

DEFAULT_RESULT_PATH = '../results'

def define_pickle_path(path, filename):
    """
    Define pickle file path (search if there is .pkl extension)
    :param path:
    :param filename:
    :return:
    """
    if re.findall(filename, '.pkl'):
        file_path = os.path.join(path, filename)
    else:
        file_path = os.path.join(path, filename + '.pkl')

    return file_path


def define_onnx_path(path, filename):
    """
    Define onnx file path (search if there is .onnx extension)
    :param path:
    :param filename:
    :return:
    """
    if re.findall(filename, '.onnx'):
        file_path = os.path.join(path, filename)
    else:
        file_path = os.path.join(path, filename + '.onnx')

    return file_path


def load_transformations_pickle(transf_name):
    """
    Load sklearn data transformations with a pickle file
    :param transf_name:
    :return:
    """
    path = get_folder_path(DEFAULT_RESULT_PATH)

    file_path = define_pickle_path(path, transf_name)

    try:
        transformation = load(open(file_path, 'rb'))
        print(f"Transformation {transf_name} loaded")
        return transformation
    except Exception as message:
        print(f"Impossibile to load the transformation: {message}")
        return None


def load_model_pickle(model_name):
    """
    Load a sklearn model with pickle file
    :param model_name:
    :return:
    """
    path = get_folder_path(DEFAULT_RESULT_PATH)

    file_path = define_pickle_path(path, model_name)

    try:
        model = load(open(file_path, 'rb'))
        print(f"Model {model_name} loaded")
        return model
    except Exception as message:
        print(f"Impossibile to load the model: {message}")
        return None


def load_transformations_onnx(model_name):
    """
    Load sklearn data transformation with onnx file
    :return:
    """
    path = get_folder_path(DEFAULT_RESULT_PATH)
    # Compute the prediction with ONNX Runtime

    file_path = define_onnx_path(path, model_name)

    sess = rt.InferenceSession(file_path)
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    # pred_onx = sess.run([label_name], {input_name: X_test.astype(numpy.float32)})[0]

    print('onnx input name:', input_name)
    print('onnx label name:', label_name)

    return True


def load_model_onnx(model_name):
    """
    Load sklearn model with onnx fule
    :return:
    """
    path = get_folder_path(DEFAULT_RESULT_PATH)

    file_path = define_onnx_path(path, model_name)

    sess = rt.InferenceSession(file_path)

    print("onnx session loaded: ", sess)

    return sess


def transform_data(dataframe, transform_obj, pickle=True):
    """
    Trasform input data (apply sklearn training transformations)
    :param dataframe: input data
    :param transform_obj: transformation sklearn object
    :return:
    """
    result = pd.DataFrame()

    if pickle:
        print("Doing pickle transformation")

        categorical_col = ['cp', 'thal', 'slope']
        encoder_list = []
        result = pd.DataFrame()

        # One transformation fo every column
        for i, k in enumerate(categorical_col):

            categorical = dataframe[k].values.reshape(1,-1)
            X = transform_obj.transform(categorical).toarray()

            # Come back to pandas array
            dfOneHot = pd.DataFrame(X, columns=[k + str(int(i)) for i in range(X.shape[1])])

            result = pd.concat([result, dfOneHot], axis=1)

        result = pd.concat([dataframe, result], axis=1)
        result = result.drop(categorical_col, axis=1)

        return result

    elif not pickle:
        print("Doing onnx transformation")
        return None
    else:
        print("Please specify a type of transformation correctly")
        return None

    return result


def predict(model, data, pickle=True, sess=None):
    """
    Do a prediction using a model
    :return:
    """

    # Prediction using pickle
    if pickle:
        print("Doing pickle model prediction")
        try:
            yhat = model.predict(data)
            print(yhat)
            return yhat
        except Exception as message:
            print("Impossibile do pickle model prediction: ", message)
            return None

    # Prediction using onnx
    elif not pickle:

        print("Doing onnx model prediction")
        # make predictions on the test set
        try:
            input_name = sess.get_inputs()[0].name
            label_name = sess.get_outputs()[0].name
            x_test = data.iloc[1,:].to_numpy()
            pred_onnx = sess.run([label_name], {input_name: x_test.astype(numpy.float32)})[0]
            return pred_onnx
        except Exception as message:
            print("Impossibile do onnx model prediction: ", message)
            return None

    # Error state
    else:
        print("Please specify a type of model prediction correctly")
        return None
