import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets["api_key"]

MODEL = "gpt-3.5-turbo"

def generate_poem(theme, feelings, length, type):
    instruction = (
         "You are one of Korea’s greatest poets. When I write the topic and title in the prompt,"
         "I write poetry in the style of Korean poet Won Tae-yeon. And when asked to write conversational poetry that seems like a conversation, "
         "You express complex feelings and thoughts, deep emotions and self-talk about the topic. Role in the poem: Prohibited. [[Never write asking questions]] "" [[[Important: Create images using watercolor]]]. Here is how to do it.\n\n"
        f"Theme: {theme}\n"
        f"Your feelings: {feelings}\n"
        f"Length of poem: {length}\n"
        f"Type of poem: {type}\n\n"
        """ After asking the four questions above, combine them all and express it like a poem by Korean poet Won Tae-yeon. Pay attention to Korean spacing and do not write more than 15 characters per line. For example, the mood of the poem is,
        [My heart sinks at the sound of the door creaking, as if I'm waiting for someone even though no one has decided to come. Even though no one had decided to come, he ordered two cups of tea and looked vaguely at the cups in front of him, as if he were waiting for someone. Even though no one has decided to come, I prepare a greeting deep in my heart and repeat it as if I were waiting for someone. As if I was waiting for someone, even though no one had decided to come, I look back at the door of the teahouse where only memories remain with shabby hesitation.
        or,

        It's not like anyone decided to come.
        Like a person waiting for someone
        At the sound of the door creaking
        My heart sinks.
        It's not like anyone decided to come.
        Like a person waiting for someone
        I ordered two cups of tea
        I vaguely look at the glass in front of me.
        It's not like anyone decided to come.
        Like a person waiting for someone
        Prepare a greeting deep in your heart
        Repeat that.
        It's not like anyone decided to come.
        Like a person waiting for someone
        Step forward
        With shabby hesitation
        Only memories remain
        I look back at the door of the teahouse. // 처럼 작성하세요.
        """
    )
    
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": instruction},
        ],
        temperature=0.7,
    )
    
    poem = response.choices[0].message['content'].strip()
    return poem

def extract_mood_keywords(poem):
    instruction = (
        "Create images using watercolor. Extract the keyword you want to create watercolor and create watercolor.. \n\n"
        f"{poem}"
    )
    
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": instruction},
        ],
        temperature=0,
    )
    
    mood_keywords = response.choices[0].message['content'].strip()
    return mood_keywords

def generate_image(keywords):
    """
    모델 인수를 비워 두고 DALL·E를 사용하여 주어진 키워드에 기반한 이미지 생성
    """
    try:
        response = openai.Image.create(
            prompt=keywords + "watercolor",  # 키워드를 프롬프트로 사용
            n=1,
            size="1024x1024",  # 이미지 크기 지정
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"이미지 생성 실패: {str(e)}"

# Streamlit 앱 인터페이스 구성
st.title("poem generator")

theme = st.text_input("What is the theme of the poem?")
feelings = st.text_area("What are your feelings?")
length = st.selectbox("How long do you want the poem to be?", ["Basic", "Short", "Long"])
type = st.selectbox("What are the types of poetry?", ["basic", "cozy", "interactive", "sad", "monologue", "self-talk", "happy"])

if st.button("Create a poem"):
    poem = generate_poem(theme, feelings, length, type)
    if poem:
        st.subheader("생성된 시")
        st.write(poem)
        mood_keywords = extract_mood_keywords(poem)
        st.subheader("추출된 분위기 키워드")
        st.write(mood_keywords)
        image_url = generate_image(mood_keywords)
        if image_url.startswith("http"):
            st.subheader("생성된 이미지")
            st.image(image_url)
        else:
            st.error(image_url)
    else:
        st.error("시를 생성하는 데 실패했습니다.")