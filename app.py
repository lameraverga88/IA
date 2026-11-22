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
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.io",
            "X-Title": "Mi Agente Multi-IA",
        }

        with st.spinner("Buscando una IA gratuita disponible..."):
            try:
                # 1. Obtiene todos los modelos gratuitos activos
                res_modelos = requests.get(
                    "https://openrouter.ai",
                    headers=headers,
                    timeout=15,
                )
                if res_modelos.status_code != 200:
                    st.error(
                        f"Error al consultar modelos ({res_modelos.status_code}): {res_modelos.text}"
                    )
                    st.stop()

                modelos_gratis = [
                    m["id"]
                    for m in res_modelos.json().get("data", [])
                    if m["id"].endswith(":free")
                ]

                if not modelos_gratis:
                    st.error("No se encontraron modelos ':free' disponibles.")
                    st.stop()

                # 2. Mezcla la lista al azar y prueba hasta encontrar uno que responda bien
                random.shuffle(modelos_gratis)
                exito = False

                for modelo_elegido in modelos_gratis[:6]:  # Prueba hasta 6 modelos al azar si alguno está saturado
                    payload = {
                        "model": modelo_elegido,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                    res_chat = requests.post(
                        "https://openrouter.ai",
                        headers=headers,
                        json=payload,
                        timeout=30,
                    )

                    if res_chat.status_code == 200 and res_chat.text.strip():
                        datos = res_chat.json()
                        if (
                            "choices" in datos
                            and len(datos["choices"]) > 0
                        ):
                            texto = datos["choices"]["message"]["content"]
                            if texto:
                                st.chat_message("assistant").markdown(
                                    f"**[Respondido por: `{modelo_elegido}`]**\n\n{texto}"
                                )
                                exito = True
                                break

                if not exito:
                    st.error(
                        "Varios modelos gratuitos están saturados en este momento. Intenta enviar el mensaje de nuevo."
                    )

            except Exception as e:
                st.error(f"Error de conexión: {e}")
