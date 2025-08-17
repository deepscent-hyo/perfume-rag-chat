# ui.py
import streamlit as st
import requests
import os, streamlit as st, requests
URL = st.secrets.get("API_URL") or os.getenv("API_URL") or "https://awqd7zegwsp7psombugpqvilrq0tdvoz.lambda-url.ap-northeast-2.on.aws/ask"

st.set_page_config(page_title="Deepscent 향 챗봇", page_icon="🧴")

st.title("🧴Deepscent 향 챗봇")

if "history" not in st.session_state:
    st.session_state["history"] = []

# --- 채팅 메시지 출력 (위에서 아래로) ---
for item in st.session_state["history"]:
    with st.chat_message("user"):
        st.markdown(item["question"])
    with st.chat_message("assistant"):
        st.markdown(item["answer"])

# --- 입력창 (항상 맨 아래) ---
if prompt := st.chat_input("향수에 대한 질문을 입력해보세요"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with ((st.chat_message("assistant"))):
        with st.spinner("향수 데이터를 검색 중..."):
            try:
                res = requests.post(URL, json={"question": prompt})
                data = res.json()  # JSON 아니면 ValueError
                answer = data.get("answer") if isinstance(data, dict) else str(data)
                if not answer:
                    answer = f"⚠️ 서버 응답에 'answer'가 없습니다. 원본: {data}"
            except Exception as e:
                answer = f"❌ 오류가 발생했습니다: {e}"

        # st.markdown(answer)

    # 기록 저장
    st.session_state["history"].append({
        "question": prompt,
        "answer": answer
    })

    st.rerun()
