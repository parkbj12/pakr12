##### 기본 정보 입력 #####
import streamlit as st
# audiorecorder 패키지 추가
from audiorecorder import audiorecorder
# OpenAI 패키기 추가
import openai
# 파일 삭제를 위한 패키지 추가
import os
# 시간 정보를 위핸 패키지 추가
from datetime import datetime
# 오디오 array 비교를 위한 numpy 패키지 추가
import numpy as np
# TTS 패키기 추가
from gtts import gTTS
# 음원파일 재생을 위한 패키지 추가
import base64



##### 기능 구현 함수 #####
def STT(audio):
    # 파일 저장
    filename='input.mp3'
    wav_file = open(filename, "wb")
    wav_file.write(audio.tobytes())
    wav_file.close()

    # 음원 파일 열기
    audio_file = open(filename, "rb")
    #Whisper 모델을 활용해 텍스트 얻기
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    # 파일 삭제
    os.remove(filename)
    return transcript["text"]

def ask_gpt(prompt, model):
    response = openai.ChatCompletion.create(model=model, messages=prompt)
    system_message = response["choices"][0]["message"]
    return system_message["content"]

##### 메인 함수 #####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="짭 GPT",
        layout="wide")

    flag_start = False
# 실습문제 5번
    # session state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

    if "check_audio" not in st.session_state:
        st.session_state["check_audio"] = []


# 실습문제 4번
    # 제목 
    st.header("짭 GPT")
    # 구분선
    st.markdown("---")

    # 기본 설명
    with st.expander("짭 GPT 설명", expanded=True):
        st.write(
        """     
        - 팀원 이름: 박병관, 홍유택
        - GPT보다 아쉬운 점이 많아 짭 GPT로 짓게 되었습니다.
        - 텍스트 버튼보다 편리하기 때문에 엔터를 눌렀을 때 답변이 출력되게 만들었습니다.
        """
        )

        st.markdown("")

    # 사이드바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        openai.api_key = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")

        # GPT 모델을 선택하기 위한 라디오 버튼 생성
        model = st.radio(label="GPT 모델",options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋 코드 
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

    # 기능 구현 공간
    col1, col2 = st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("질문하기")
        # 음성 녹음 아이콘 추가 / 실습문제 6번
        audio = audiorecorder("음성 질문", "녹음중...")
        if len(audio) > 0 and not np.array_equal(audio,st.session_state["check_audio"]):
            # 음성 재생 
            st.audio(audio.tobytes())

            # 음원 파일에서 텍스트 추출 / 실습문제 7번
            question = STT(audio)

            # 채팅을 시각화하기 위해 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("user",now, question)]
            # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "user", "content": question}]
            # audio 버퍼 확인을 위해 현 시점 오디오 정보 저장
            st.session_state["check_audio"] = audio
            flag_start =True

        st.markdown("---")
        # 텍스트 아이콘 추가
        text_question = st.text_area("질문을 입력하세요", "")
        if st.button("텍스트 질문"):
            if text_question.strip() != "":
                now = datetime.now().strftime("%H:%M")
                st.session_state["chat"] = st.session_state["chat"]+ [("user",now, text_question)]
                # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
                st.session_state["messages"] = st.session_state["messages"]+ [{"role": "user", "content": text_question}]
                flag_start =True

    with col2:
        # 오른쪽 영역 작성
        st.subheader("질문/답변")
        if flag_start:
            #ChatGPT에게 답변 얻기 / 실습문제 8번
            response = ask_gpt(st.session_state["messages"], model)

            # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "system", "content": response}]

            # 채팅 시각화를 위한 답변 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("bot",now, response)]

            # 채팅 형식으로 시각화 하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:green;color:white;border-radius:12px;padding:8px 8px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray; >{time}</div></div>', unsafe_allow_html=True)
                    
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end width = "30px";"><div style="background-color:blue;border-radius:12px;padding:4px 8px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

if __name__=="__main__":
    main()