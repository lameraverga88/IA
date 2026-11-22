import random
import requests
import streamlit as st

st.title("Mi Agente Multi-IA en la Nube")

api_key = st.sidebar.text_input("OpenRouter API Key", type="password")

# Lista directa de modelos gratuitos activos (sin hacer GET previo)
MODELOS_GRATIS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-3-27b-it:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "deepseek/deepseek-r1:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
]

if prompt := st.chat_input("Escribe tu consulta..."):
    if not api_key:
        st.warning("Por favor ingresa tu API Key de OpenRouter a la izquierda.")
    else:
        st.chat_message("user").write(prompt)
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.io",
            "X-Title": "Agente Multi-IA",
        }

        with st.spinner("Consultando modelos gratuitos al azar..."):
            candidatos = MODELOS_GRATIS.copy()
            random.shuffle(candidatos)
            exito = False
            ultimo_error = ""

            for modelo in candidatos:
                try:
                    res = requests.post(
                        "https://openrouter.ai",
                        headers=headers,
                        json={
                            "model": modelo,
                            "messages": [{"role": "user", "content": prompt}],
                        },
                        timeout=25,
                    )

                    if res.status_code == 200 and res.text.strip():
                        datos = res.json()
                        if "choices" in datos and len(datos["choices"]) > 0:
                            texto = datos["choices"]["message"]["content"]
                            st.chat_message("assistant").markdown(
                                f"**[Respondido por: `{modelo}`]**\n\n{texto}"
                            )
                            exito = True
                            break
                    else:
                        ultimo_error = f"Código {res.status_code} en {modelo}: {res.text[:200]}"
                except Exception as e:
                    ultimo_error = f"Fallo en {modelo}: {e}"

            if not exito:
                st.error(
                    f"Ningún modelo respondió. Último detalle: {ultimo_error}"
                )
