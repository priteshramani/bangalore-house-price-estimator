import streamlit as st
import pickle
import json
import numpy as np

# Load artifacts
def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    if __model is None:
        with open('model.pickle', 'rb') as f:
            __model = pickle.load(f)

# Predict function
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

# Run the app
def main():
    st.title("🏠 Bangalore Home Price Estimator")

    sqft = st.number_input("Area (Square Feet)", 500, 10000, step=50)
    bhk = st.radio("BHK", [1, 2, 3, 4, 5], horizontal=True)
    bath = st.radio("Bath", [1, 2, 3, 4, 5], horizontal=True)
    location = st.selectbox("Location", __locations)

    if st.button("Estimate Price"):
        price = get_estimated_price(location, sqft, bhk, bath)
        st.success(f"🏷️ Estimated Price: {price} Lakh")

# Load model + run app
if __name__ == '__main__':
    __model = None
    load_saved_artifacts()
    main()
