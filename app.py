import streamlit as st
import requests
import json

# Gemini API Setup
API_KEY = "AIzaSyBhqXGiQRyPPkcG2uL-zNdwNdTSGStonGo"  # Replace with your actual Gemini API key
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_gemini_response(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    params = {"key": API_KEY}

    try:
        response = requests.post(URL, headers=headers, params=params, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", None)
        return generated_text or "No response from Gemini."
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"

# Streamlit App UI
st.set_page_config(page_title="Algorithm Explainer", page_icon="🧠")
st.title("🧠 Algorithm Explainer")
st.markdown("Explain any algorithm in a beginner-friendly way with examples and code!")

algorithm = st.text_input("🔍 Enter the name of an algorithm (e.g., Bubble Sort, Dijkstra, Backpropagation):")

if st.button("Explain Algorithm"):
    if algorithm.strip() == "":
        st.error("Please enter a valid algorithm name.")
    else:
        with st.spinner("Thinking... 🧠"):
            prompt = f"""
You are a Computer Science professor. Explain the algorithm "{algorithm}" to a beginner student. 
Structure your response in the following format:

1. ✏️ Explanation: A clear, simple explanation of how the algorithm works.
2. 🧮 Time and Space Complexity: Give both best-case and worst-case complexities.
3. 💡 Analogy: A real-life analogy if possible.
4. 💻 Python Code: A working example in Python.

Keep it friendly and easy to follow.
            """
            response = generate_gemini_response(prompt)

        if response:
            st.markdown("---")
            st.subheader(f"📘 Explanation for: `{algorithm}`")
            st.markdown(response)
        else:
            st.warning("Gemini did not return a valid explanation.")
    