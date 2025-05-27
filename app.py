import streamlit as st
import requests
import fitz  # PyMuPDF
import docx

# --- Functions ---

def extract_text(file, filetype):
    if filetype == "txt":
        return file.read().decode("utf-8")
    elif filetype == "pdf":
        text = ""
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif filetype == "docx":
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return file.read().decode("utf-8")

def call_ollama(model, prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return None

def get_file_extension(language):
    ext_map = {
        "Python": "py",
        "JavaScript": "js",
        "Java": "java",
        "C++": "cpp",
        "C": "c",
        "Go": "go",
        "Ruby": "rb",
        "TypeScript": "ts"
    }
    return ext_map.get(language, "txt")

# --- Streamlit UI ---

st.set_page_config(page_title="Multiformat Code Translator", layout="wide")
st.title("📤 Code Translator ")

uploaded_file = st.file_uploader("Upload a code or text document", type=["py", "js", "java", "cpp", "c", "ts", "rb", "go", "txt", "pdf", "docx"])
target_language = st.selectbox("Select Target Language", ["Python", "JavaScript", "Java", "C++", "C", "Go", "Ruby", "TypeScript"])

if uploaded_file and target_language:
    filetype = uploaded_file.name.split(".")[-1]
    original_code = extract_text(uploaded_file, filetype)

    if original_code:
        # 🔘 Button to trigger translation
        if st.button("🚀 Convert"):
            # Show original code in center
            st.markdown("<h4 style='text-align: center;'>📄 Original Code/Text</h4>", unsafe_allow_html=True)
            st.code(original_code, language="auto")

            # --- Translate the Code ---
            translation_prompt = f"Translate the following code or content into {target_language}:\n\n```{original_code}```"
            with st.spinner("🔁 Translating code..."):
                translated_code = call_ollama("codellama", translation_prompt)

            if translated_code:
                # --- Generate Documentation and Run Instructions ---
                doc_prompt = f"""Explain what the following {target_language} code does. Provide documentation-style summary with key functions, logic flow, and purpose.\n\n```{translated_code}```"""
                run_prompt = f"""Provide detailed, step-by-step instructions to run the following {target_language} code. Include required tools, dependencies, and commands:\n\n```{translated_code}```"""

                with st.spinner("📘 Generating documentation and run steps..."):
                    code_doc = call_ollama("llama3", doc_prompt)
                    run_steps = call_ollama("llama3", run_prompt)

                # 🧱 Two-column layout below original code
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🔁 Translated Code")
                    st.code(translated_code, language=target_language.lower())

                    ext = get_file_extension(target_language)
                    st.download_button(
                        label="💾 Download Translated Code",
                        data=translated_code,
                        file_name=f"translated_program.{ext}",
                        mime="text/plain"
                    )

                with col2:
                    st.subheader("📘 Code Documentation")
                    if code_doc:
                        st.markdown(code_doc)
                    else:
                        st.error("⚠️ Failed to generate documentation.")

                    st.markdown("---")

                    st.subheader("🛠️ How to Run the Code")
                    if run_steps:
                        st.markdown(run_steps)
                    else:
                        st.error("⚠️ Failed to generate run steps.")
            else:
                st.error("❌ Translation failed. Check if CodeLlama is running.")
    else:
        st.warning("⚠️ Could not read the uploaded file content.")
