import pandas as pd
import streamlit as st
import base64
from resources.backend_functions import load_model_pickle, \
    load_transformations_pickle, load_model_onnx, load_transformations_onnx, predict, transform_data


def side_menu(model, transform):
    """
    Streamlit side menù configuration
    :return:
    """
    st.sidebar.markdown("### **Configuration Pannel**")

    st.sidebar.markdown("**Set parameters for the model**")
    age = st.sidebar.number_input('Age', value=40)
    sex = st.sidebar.number_input('Sex', value=1)
    cp = st.sidebar.number_input('CP', value=2)
    trestbps = st.sidebar.number_input('Trestbps', value=101)
    chol = st.sidebar.number_input('Chol', value=228)
    fbs = st.sidebar.number_input('fbs', value=1)
    restecg = st.sidebar.number_input('restecg', value=1)
    thalach = st.sidebar.number_input('thalach', value=1)
    exang = st.sidebar.number_input('exang', value=1)
    oldpeak = st.sidebar.number_input('oldpeak', value=1)
    slope = st.sidebar.number_input('slope', value=1)
    ca = st.sidebar.number_input('ca', value=1)
    thal = st.sidebar.number_input('thal', value=1)

    input_values = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

    if st.sidebar.button('Predict'):
        colnames = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        input_data = pd.DataFrame(columns=colnames)
        input_data.loc[0] = input_values

        # TODO: Fix this
        # input_data = transform_data(input_data,transform)

        result = predict(model, input_data)

        input_data['PredictionResult'] = result[0]
        return input_data, result
    else:
        st.sidebar.text('Please press \"Predict\" to run')
        result = None
        return None, result


def main():
    """
    Main function of the program
    :return: 
    """
    model = load_model_pickle('knn')
    transform = load_transformations_pickle('MinMax')

    input_data, result = side_menu(model, transform)

    if result is not None:

        # Visualize the result
        result_string = f"### **Prediction Result:** {result}"
        st.text('\n')
        st.markdown(result_string)

        # Save to csv
        csv = input_data.to_csv(index=True)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.text('\n')
        st.markdown('Press "Predict" for a prediction')

    return True


if __name__ == '__main__':
    print("--Streamlit test run--")

    st.title('Heart desease prediction')
    st.markdown('## Predict a hearth desease based on certain parameters')
    st.markdown('Please insert the parameters on the sidebar and launch the prediction')
    st.markdown('**Data contains**')
    st.markdown('* **age** - age in years')
    st.markdown('* **sex** - (1 = male; 0 = female)')
    st.markdown('* **cp** - chest pain type')
    st.markdown('* **trestbps** - resting blood pressure (in mm Hg on admission to the hospital)')
    st.markdown('* **chol** - serum cholestoral in mg/dl')
    st.markdown('* **fbs** - (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)')
    st.markdown('* **restecg** - resting electrocardiographic results')
    st.markdown('* **thalach** - maximum heart rate achieved')
    st.markdown('* **exang** - exercise induced angina (1 = yes; 0 = no)')
    st.markdown('* **oldpeak** - ST depression induced by exercise relative to rest')
    st.markdown('* **slope** - the slope of the peak exercise ST segment')
    st.markdown('* **ca** - number of major vessels (0-3) colored by flourosopy')
    st.markdown('* **thal** - 3 = normal; 6 = fixed defect; 7 = reversable defect')
    st.markdown('* **target** - have disease or not (1=yes, 0=no)""")')

    # Launch the main
    main()
