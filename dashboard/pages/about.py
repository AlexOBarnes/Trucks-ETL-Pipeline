'''About section on the T3 trucks data dashboard'''
import streamlit as st

if __name__ == "__main__":
    st. set_page_config(layout="wide")
    st.title("About Us")
    st.subheader("Serving Delectable Delights on Wheels!")

    st.write("""
        **Tasty Truck Treats (T3)** is a catering company that specializes in operating a fleet of food trucks in Lichfield and its surrounding areas.
        Dedicated to delivering diverse and delicious culinary experiences, T3 takes pride in serving a wide range of delectable treats to cater to 
        different tastes and preferences.
        """)

    st.header("Our Unique Food Trucks")
    st.write("""
        Each food truck in T3’s fleet operates semi-independently, with its own unique menu and style. Whether you're in the mood for gourmet burgers, 
        sandwiches, mouthwatering desserts, or refreshing beverages, T3 has something for every craving. 

        Our diverse range of food offerings ensures that there’s always something exciting to try, no matter what you're in the mood for!
        """)

    st.header("Strategic Locations")
    st.write("""
        T3's food trucks are strategically stationed at popular locations throughout Lichfield and its surrounding areas. 
        From bustling city areas to office complexes and event venues, our trucks are easily accessible to a wide range of customers.

        Whether you're on your lunch break or attending an outdoor event, you're sure to spot one of our vibrant trucks nearby.
        """)


    st.header("Eye-Catching Trucks & Exceptional Service")
    st.write("""
        At T3, we believe that the food experience starts even before you take your first bite. Our trucks are designed to be visually inviting, featuring 
        vibrant branding, enticing menu displays, and a welcoming atmosphere created by our friendly staff members.

        Exceptional customer service is at the heart of what we do, and we strive to make every dining experience memorable.
        """)


    st.header("Contact Us")
    st.write("""
        Want to learn more or book one of our food trucks for an event? Feel free to get in touch!

        - **Website**: [www.tastytrucktreats.com](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
        - **Phone**: 020 5555 5555
        - **Address**: 45 Fake St., Lichfield, UK
        """)
