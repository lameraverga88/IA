import random
import requests
import streamlit as st

st.title("Mi Agente Multi-IA en la Nube")

st.sidebar.header("Claves API Gratuitas")
groq_key = st.sidebar.text_input(
    "Groq API Key (://groq.com)", type="password"
)
gemini_key = st.sidebar.text_input(
    "Gemini API Key (://google.com)", type="password"
)

if prompt := st.chat_input("Escribe tu consulta..."):
    if not groq_key and not gemini_key:
        st.warning(
            "Ingresa al menos una clave gratuita (Groq o Gemini) en la barra izquierda."
        )
    else:
        st.chat_message("user").write(prompt)

        # Armamos la lista de IAs disponibles según las claves que pusiste
        opciones_ia = []
        if groq_key:
            opciones_ia.extend([
                ("Groq - Llama 3.3 70B", "groq", "llama-3.3-70b-versatile"),
                ("Groq - Llama 3.1 8B", "groq", "llama-3.1-8b-instant"),
                ("Groq - Qwen QwQ 32B", "groq", "qwen-qwq-32b"),
            ])
        if gemini_key:
            opciones_ia.extend([
                ("Google - Gemini 2.5 Flash", "gemini", "gemini-2.5-flash"),
                (
                    "Google - Gemini 2.5 Flash Lite",
                    "gemini",
                    "gemini-2.5-flash-lite",
                ),
            ])

        # Elige una IA al azar entre todas las disponibles
        nombre_ia, proveedor, modelo_id = random.choice(opciones_ia)

        with st.spinner(f"Enrutando al azar a {nombre_ia}..."):
            try:
                if proveedor == "groq":
                    res = requests.post(
                        "https://groq.com",
                        headers={
                            "Authorization": f"Bearer {groq_key.strip()}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": modelo_id,
                            "messages": [{"role": "user", "content": prompt}],
                        },
                        timeout=25,
                    )
                    datos = res.json()
                    if "choices" in datos:
                        texto = datos["choices"]["message"]["content"]
                        st.chat_message("assistant").markdown(
                            f"**[Respondido al azar por: `{nombre_ia}`]**\n\n{texto}"
                        )
                    else:
                        st.error(f"Error de Groq: {datos}")

                elif proveedor == "gemini":
                    url = f"https://googleapis.com{modelo_id}:generateContent?key={gemini_key.strip()}"
                    res = requests.post(
                        url,
                        headers={"Content-Type": "application/json"},
                        json={"contents": [{"parts": [{"text": prompt}]}]},
                        timeout=25,
                    )
                    datos = res.json()
                    if "candidates" in datos:
                        texto = datos["candidates"]["content"]["parts"][
                            "text"
                        ]
                        st.chat_message("assistant").markdown(
                            f"**[Respondido al azar por: `{nombre_ia}`]**\n\n{texto}"
                        )
                    else:
                        st.error(f"Error de Gemini: {datos}")

            except Exception as e:
                st.error(f"Error de conexión: {e}")
