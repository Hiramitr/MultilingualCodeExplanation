import requests
import streamlit as st

HUGGINGFACE_API_KEY = "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"  # Replace with your actual API key
API_URL = r"https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
# API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_llama3(input_text, language):
   # Create the prompt
   prompt = (
       f"Provide a simple explanation of this code in {language}:\n\n{input_text}\n"
       f"Only output the explanation and nothing else. Make sure that the output is written in {language} and only in {language}"
   )
   # Payload for the API
   payload = {
       "inputs": prompt,
       "parameters": {"max_new_tokens": 500, "temperature": 0.3},
   }
  
   # Make the API request
   response = requests.post(API_URL, headers=HEADERS, json=payload)
   if response.status_code == 200:
       result = response.json()
      
       # Extract the response text
       full_response = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
      
       # Clean up: Remove the prompt itself from the response
       clean_response = full_response.replace(prompt, "").strip()
       # Further clean any leading colons or formatting
       if ":" in clean_response:
           clean_response = clean_response.split(":", 1)[-1].strip()
      
       return clean_response or "No explanation available."
   else:
       return f"Error: {response.status_code} - {response.text}"
    
if __name__ == "__main__":

    # Side bar components
    st.set_page_config(page_title="コード説明AI（日本語非対応）", layout="wide")
    st.sidebar.title("このアプリについて")
    st.sidebar.markdown("""
    1. フロントエンド　: Streamlit
                        Pythonコードで簡単にウェブアプリを作成するためのライブラリ。
                        大規模なアプリ（ページ数が多い、アクセスするユーザが多い）の構築には向いていない

    2. API：HuggingFaceのウェブAPI（RESTful API）
            AIモデルプラットフォームのHuggingFaceのサイトにアクセスしてAIモデルを使用する
                        
    3. AI：Meta-Llama-3-8B
            Meta社の無償で使えるLLM
    """)
    st.sidebar.divider()
    st.sidebar.markdown(
    """
    <div style="text-align: center;color: grey;">
        平光 凌大 (Ryota Hiramitsu)
    </div>
    """,
    unsafe_allow_html=True
    )

    # Main app components
    st.title("コード説明AI（日本語非対応）")
    st.markdown("### Powered by Meta-Llama-3-8B-Instruct from Hugging Face")

    # Input fields
    code_snippet = st.text_area("Paste your code snippet here:", height=200)
    preferred_language = st.text_input("Enter your preferred language for explanation (e.g., English, Spanish):")

    # Generate explanation buttona
    if st.button("送信"):
        if code_snippet and preferred_language:
            with st.spinner("Generating explanation... ⏳"):
                explanation = query_llama3(code_snippet, preferred_language)
            st.subheader("Generated Explanation:")
            st.write(explanation)
        else:
            st.warning("⚠️ Please provide both the code snippet and preferred language.")

    # Footer
    st.markdown("---")
#    st.markdown("🧠 **Note**: This app uses Meta-Llama-3-8B-Instruct from Hugging Face for multilingual code explanations.")