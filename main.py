from google.cloud import texttospeech
from google.oauth2 import service_account

import io
import streamlit as st

creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

def synthesize_speech(text,language = '日本語', gend = 'default',):
    genderType = {
    'デフォルト': {'name': None, 'gender': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED},
    '男性': {'name': 'ja-JP-Wavenet-C', 'gender': texttospeech.SsmlVoiceGender.MALE},
    '女性': {'name': 'ja-JP-Wavenet-A', 'gender': texttospeech.SsmlVoiceGender.FEMALE},
    '中性': {'name': None, 'gender': texttospeech.SsmlVoiceGender.NEUTRAL}
    }

    languages = {
            '日本語': 'ja-JP',
            '英語': 'en-US',
    }

    Gender = gend
    genders = genderType[Gender]
    Name = genders['name']
    gender = genders['gender']

    lang = language

    client = texttospeech.TextToSpeechClient(credentials=creds)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        name = Name,
        language_code=languages[lang],
        ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response

st.title('音声出力アプリ')

st.markdown('### データの準備')

input_option = st.selectbox(
    '入力データの選択',
    ('直接入力', 'テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力してください', 'これはサンプル文です')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)
    st.markdown('### パラメータ設定')
    st.subheader('話者の性別選択')

    lang = st.selectbox(
        '言語を選択してください',
        ('日本語', '英語')
    )

    gender = st.selectbox(
        '話者の性別を選択してください',
        ('デフォルト', '男性', '女性', '中性')
    )
    st.markdown('### 音声生成')
    st.write('こちらの文章で音声生成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        
        response = synthesize_speech(input_data, lang, gender)
        st.audio(response.audio_content)
        comment.write('完了')