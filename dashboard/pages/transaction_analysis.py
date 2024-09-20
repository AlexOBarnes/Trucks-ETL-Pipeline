'''Streamlit dashboard for transaction analysis page'''
#pylint: disable=import-error
import streamlit as st
from graphs import make_payment_graphs

if __name__ == "__main__":
    st. set_page_config(layout="wide")
    st.title("Payment Method Analytics")
    with st.sidebar:
        selected_type = st.multiselect("Truck", ["card","cash"],["card","cash"])

    proportion, value_per_payment_type = make_payment_graphs(selected_type)

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(proportion, use_container_width=True)
    with col2:
        st.altair_chart(value_per_payment_type, use_container_width=True)
