import os
from openai import OpenAI
import streamlit as st

st.title("SatanaS")

# Pide tu API Key gratuita de OpenRouter en la barra lateral
api_key = st.sidebar.text_input("OpenRouter API Key", type="password")

if prompt := st.chat_input("Ordene Patron..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key de OpenRouter a la izquierda.")
    else:
        client = OpenAI(
            base_url="https://openrouter.ai",
            api_key=api_key,
        )
        st.chat_message("user").write(prompt)
        with st.spinner("Enrutando a la mejor IA gratuita..."):
            respuesta = client.chat.completions.create(
                model="openrouter/free",
                messages=[{"role": "user", "content": prompt}],
            )
            st.chat_message("assistant").write(
                respuesta.choices[0].message.content
            )
