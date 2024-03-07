import streamlit as st
from utils import generate_image


st.title("AI Image generator")

with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API key to get started:", type="password")

image_desc = st.text_input("Describe your image (e.g. ballet dancers posing on a beam):")
image_style = st.text_input("Enter the image style (e.g. romantic impressionist painting):")
refinement_enabled = st.checkbox("Let AI refine your image description before generating.")
image_size = st.selectbox("Select the image size:",
                          ["1024x1024", "1024x1792", "1792x1024"])

st.divider()
submitted = st.button("Generate your image!")

if submitted and not api_key:
    st.info("API key is missing!")
    st.stop()
if submitted and not image_desc:
    st.info("Image description is missing!")
    st.stop()
if submitted and not image_style:
    st.info("Image style is missing!")
    st.stop()
if submitted:
    with st.spinner("Generating something amazing for you..."):
        image_url, refined_desc = generate_image(image_desc, image_style, image_size, refinement_enabled, api_key)
    st.success("Generated successfully!")
    st.subheader("Image description:")
    st.write(refined_desc)
    st.markdown("![image]({url})".format(url=image_url))
