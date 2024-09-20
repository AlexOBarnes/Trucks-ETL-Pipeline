'''This module creates a streamlit dashboard for the graphs contained in graphs.py'''
import streamlit as st
from graphs import make_graphs

if __name__ =="__main__":
    st. set_page_config(layout="wide")
    st.title("T3: Food Truck Analytics")
    transactions_over_time,revenue_over_time = make_graphs()

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(revenue_over_time, use_container_width=True)
    with col2:
        st.altair_chart(transactions_over_time, use_container_width=True)
