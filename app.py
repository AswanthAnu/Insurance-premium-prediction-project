import streamlit as st
import numpy as np
import pandas as pd
import pickle

model = pickle.load(open('model.pkl', 'rb')) 
encoder = pickle.load(open('target_encoder.pkl', 'rb')) 
transformer = pickle.load(open('transformer.pkl', 'rb'))

st.title("Insurance Premium Prediction")

Gender = st.selectbox("Select your gender", ('male', 'female'))

Age = st.text_input("Enter your Age", 23)

BMI = st.text_input("Enter your BMI", 20)
BMI = float(BMI)

Children = st.selectbox("Select number of Childrens", (0, 1, 2, 3, 4, 5, 6))
Children = int(Children)

Smoker = st.selectbox("Are you a smoker ?", ("Yes", "No"))

Region = st.selectbox("Select your region", ("southwest", "southeast",  "northeast", "northwest"))

l = {}
l['age'] = Age
l['sex'] = Gender
l['bmi'] = BMI
l['children'] = Children
l['smoker'] = Smoker
l['region'] = Region

df = pd.DataFrame(l, index = [0])

df['region'] = encoder.transform(df['region'])
df['sex'] = df['sex'].map({'male':0, "female":1})
df['smoker'] = df['smoker'].map({'Yes':1, "No":0})

df = transformer.transform(df)
y_pred = model.predict(df)

if st.button("Submit"):
    st.header(f"{round(y_pred[0], 2)} INR")