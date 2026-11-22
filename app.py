import random
from openai import OpenAI
import streamlit as st

st.title("Mi Agente Multi-IA en la Nube")

api_key = st.sidebar.text_input("OpenRouter API Key", type="password")

if prompt := st.chat_input("Escribe tu consulta..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key de OpenRouter a la izquierda.")
    else:
        client = OpenAI(
            base_url="https://openrouter.ai",
            api_key=api_key,
        )
        st.chat_message("user").write(prompt)

        with st.spinner("Buscando modelos gratuitos activos y enrutando..."):
            try:
                # 1. Obtiene en tiempo real los modelos gratuitos disponibles para tu clave
                todos_modelos = client.models.list()
                modelos_gratis = [
                    m.id for m in todos_modelos.data if m.id.endswith(":free")
                ]

                if not modelos_gratis:
                    st.error(
                        "OpenRouter no devolvió modelos ':free'. Revisa que tu API Key esté bien copiada."
                    )
                else:
                    # 2. Elige un modelo gratuito al azar (enrutamiento arbitrario real)
                    modelo_elegido = random.choice(modelos_gratis)

                    respuesta = client.chat.completions.create(
                        model=modelo_elegido,
                        messages=[{"role": "user", "content": prompt}],
                    )

                    texto = respuesta.choices[0].message.content
                    st.chat_message("assistant").markdown(
                        f"**[Respondido al azar por: `{modelo_elegido}`]**\n\n{texto}"
                    )

            except Exception as e:
                st.error(f"Detalle del error: {e}")
