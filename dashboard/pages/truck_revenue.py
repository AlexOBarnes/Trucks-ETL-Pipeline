'''Streamlit dashboard for revenue page'''
# pylint: disable=import-error
import streamlit as st
from graphs import get_truck_names, make_revenue_graphs

if __name__ == "__main__":
    truck_names = get_truck_names()
    st. set_page_config(layout="wide")
    st.title("Revenue by Truck")
    with st.sidebar:
        selected_trucks = st.multiselect("Truck", truck_names,truck_names)

    transactions_by_truck, revenue_by_truck, fsa_by_revenue =  make_revenue_graphs(selected_trucks)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.altair_chart(transactions_by_truck, use_container_width=True)
    with col2:
        st.altair_chart(revenue_by_truck, use_container_width=True)
    with col3:
        st.altair_chart(fsa_by_revenue, use_container_width=True)
