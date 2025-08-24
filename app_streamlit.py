import streamlit as st
from interpretator import run_program

st.set_page_config(page_title="Corporate Language Interpreter", layout="centered")

st.title("📝 Corporate Language Interpreter")

with st.expander("📖 Instructions", expanded=True):
    st.markdown("""
    - ➡️ Write or paste your code in **Corporate Language** below.
    - ➡️ Click **Run** to execute the code and see the output below.
    - ➡️ Demo code examples are provided — click to copy and try running them.
    """)

examples = [
    ("📝 Simple Hello", "day start\nreportKaro \"Hello duniya!\"\nday end"),
    ("✅ Condition Example", "day start\nagar (5 > 3)\n  reportKaro \"5 bada hai 3 se\"\nnahi\n  reportKaro \"3 bada hai 5 se\"\nday end"),
    ("📦 Variables", "day start\nassignTask x = 10\nassignTask y = 20\nreportKaro x\nreportKaro y\nday end"),
    ("🔁 Loop Example", "day start\nassignTask i = 1\nchalo meeting kre 3\n  reportKaro \"👥 Standup ho raha\"\nfinally over huyi\nday end"),
    ("🔥 Complex Program", "day start\n\nreportKaro \"🌞 Good morning team\"\nassignTask tas = 3 \nmanager ka mood kya he \"angry\"\nmanager ka mood\n  jab \"angry\"\n    reportKaro \"👿 Manager gussa me hai\"\n  jab \"busy\"\n    reportKaro \"📞 Manager busy bol raha\"\n  jab \"happy\"\n    reportKaro \"😎 Manager bol raha chhutti le lo\"\n  choro\n    reportKaro \"😅 Manager ka koi bharosa nahi\"\nmood ka the end\n\nassignTask tasks = 5\nagar (tasks > 3)\n  reportKaro \"📊 Kaam zyada ho gaya\"\nnahi\n  reportKaro \"👌 Chill maro\"\nkaam band\n\nchalo meeting kre 3\nreportKaro \"👥 Standup ho raha\"\nfinally over huyi\n\nclient call lagao\nreportKaro \"🚀 Code deploy kar rahe the\"\nissue aa gaya\nreportKaro \"😶 Ye line nahi chalni chahiye\"\nclient gussa hua\nagar (tasks > 10)\n  reportKaro \"🔥 Client gussa ho gaya\"\nchinta mat kar\nreportKaro \"😌 Chinta mat kar, fix ho jayega\"\nchinta over\ntea break 10\n\nday end")
]

st.subheader("🎨 Demo Examples:")
cols = st.columns(2)
for idx, (title, code) in enumerate(examples):
    with cols[idx % 2]:
        st.markdown(f"**{title}**")
        st.code(code, language="text")
        if st.button(f"📋 Copy Example {idx+1}", key=f"copy{idx}"):
            st.session_state["code"] = code

code = st.text_area("Yahan apna code likho...", value=st.session_state.get("code", ""), height=300, key="code_input")

if st.button("⚡ Run"):
    if code.strip():
        try:
            codeLine = code.splitlines()
            output_box = st.empty()
            output_lines = []
            for chunk in run_program(codeLine):
                output_lines.append(str(chunk))
                output_box.code("\n".join(output_lines), language="text")
        except Exception as e:
            output_box.code(f"Error: {e}", language="text")
    else:
        st.warning("Code likho aur Run dabao!")
else:
    st.subheader("📤 Output:")
    st.code("Code ka result yahan aayega...", language="text")
