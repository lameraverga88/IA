import random
import requests
import streamlit as st

st.title("Mi Agente Multi-IA en la Nube")

api_key = st.sidebar.text_input("OpenRouter API Key", type="password")

if prompt := st.chat_input("Escribe tu consulta..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key de OpenRouter a la izquierda.")
    else:
        st.chat_message("user").write(prompt)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        with st.spinner("Enrutando a una IA gratuita al azar..."):
            try:
                # 1. Obtiene los modelos gratuitos activos directamente desde la API
                res_modelos = requests.get(
                    "https://openrouter.ai", headers=headers
                ).json()
                modelos_gratis = [
                    m["id"]
                    for m in res_modelos.get("data", [])
                    if m["id"].endswith(":free")
                ]

                if not modelos_gratis:
                    st.error(
                        "No se encontraron modelos gratuitos. Verifica tu API Key."
                    )
                else:
                    # 2. Selecciona un modelo gratuito al azar (enrutamiento arbitrario)
                    modelo_elegido = random.choice(modelos_gratis)

                    # 3. Envía la consulta al modelo elegido
                    payload = {
                        "model": modelo_elegido,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                    res_chat = requests.post(
                        "https://openrouter.ai",
                        headers=headers,
                        json=payload,
                    ).json()

                    if "choices" in res_chat:
                        texto = res_chat["choices"]["message"]["content"]
                        st.chat_message("assistant").markdown(
                            f"**[Respondido al azar por: `{modelo_elegido}`]**\n\n{texto}"
                        )
                    else:
                        st.error(f"Respuesta de OpenRouter: {res_chat}")

            except Exception as e:
                st.error(f"Error de conexión: {e}")
