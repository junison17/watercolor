import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets["api_key"]

MODEL = "gpt-3.5-turbo"

def generate_poem(theme, feelings, length, type):
    instruction = (
         """You are one of the best poets in Korea. When I write a topic and title at a prompt, you write a poem of the original Korean poet type. And when I ask you to write a poem in dialogue that seems to be talking to each other, you write it in dialogue. The method is as follows.
Important:
1. Emotional expression (messages and expressions that readers can relate to)
2. Word Expression: Write as if you are having a natural conversation with the reader using appropriate words and colloquialisms. The emotions you want to express vary depending on the topic
3. Sentence structure: Write poems in various sentence structures without being bound by coordination ideas.
4. Do not use words or sentences that are too difficult.
5. Use interesting metaphors, appropriate metaphors, various metaphors, and metaphors related to the subject of the writing

example: 

When you write a poem, write it in the tone below,
[The content is different] [Write the mood, paragraph, and tone of the poem like the poem below]


Title: With only one memory

under only one name
I want to keep it
There will be a lot of pain
The pain
Even if you drive me crazy
Until the moment I go crazy
under only one name
I want to keep it
That one
under only one name
I want to be remembered
Even if we can't see each other again
Memories
With the longing that I never left
It's deeply ingrained in my heart
Even if it rains
Even if it's windy
without wavering
under only one name
I want to be remembered.


-----------------------------
Title: Promise

I wanted to make a country without breaking up
The heart of the person who left
I'll give you back like I did before
Even if you have a heartbreaking breakup
have a night's pain
You're going to make me forget it like a lie

If I make a promise like this
To those who are going through a breakup
I could get all the votes...
Are you kidding me
I said I wouldn't vote
I'm gonna take a picture of him right now...


Title: Being Tamed

If you're used to something
It's hard to fix
If you make that much effort
Something that's possible
If you're used to someone
It's hard to fix it
After we shed as much tears as we loved each other
even if it's possible
By then, you will already be accustomed to longing.
-----------------------------

Title: Reason

From the moment we broke up
If you cry a lot
It's because of the sadness of love that I can't finish
The person who talks a lot
That's how much I have left
The person who wants to meet many friends
Because I need somewhere to reach
I wanted to be alone
If you don't even know that your heart is broken
Because I still don't realize the breakup.


-----------------------------

Title: Waiting


After waiting for the hardest day
I'll call you
on hard days
I'm sure he's having a hard time with hesitation

I waited for the most depressing day
I'm writing to you
The longing for a gloomy day
Rather than longing for a happy day
It'll get darker on your face

with hard work
When I'm watching a depressing movie
It's sadder than tears
I'm waiting for your reply

-----------------------------

Title: Because I'm alone

There's no need to bicker.
You don't have to be upset
The sense of duty to meet
The pressure to call
And other things that made me feel frustrated
There are many reasons why it's gone.
because
Because I'm alone now.

I'll meet someone else, too.
Before, when I came in late
I was more sensible than my mom
It's okay now.
I think it's very comfortable.
But... The weird thing is
There's too much time left.
At a time when there's nothing to do
I keep thinking about it.
Come to think of it
Now...
I think it's because I'm alone.
---------------------------

Title: Because I'm alone

If it's a boring dinner time
Call me without any particular business
There was no place to talk for hours.
When I'm on a blind date
I felt a bit guilty and sorry
There's no place to make you feel good about it.

I don't think anything has changed
A lot of things look different.
There's a person who's harder to see than a popular star
Even if it hurts
Even if I have a fever
I'm in pain. Where to lean
I don't have a hand to measure my temperature
A birthday or a meaningful day
There's nothing to look forward to
It's like that again.
On Saturday afternoons or on holiday mornings
Of course, I'm supposed to be seeing you
I'm meeting my friends
When I'm watching TV
Now I realize that it's not us.
If you want to call out a name
If you want to see a face
What you need to do every time
It's dark in front of my eyes.
--------------------------

Title: I don't think it's that far away

I don't think it's that far off
When I call your name
It sounds unfamiliar
It's a name that I've called so many times...

I don't think it's that far off
When I think of your beautiful face
It's so awkward that it's sad
I've seen this face so many times...

I don't think it's that far off
I guess it's time to forget about it
I've always wanted to do this whenever I'm lonely
More than when I tried to forget
It's more heartbreaking
That's what I wanted so badly...
 ((Write it in Korean and answer it in Korean))

After asking the above four questions, write a poem by combining all of them.
[I:
You:] Omit these phrases, exclude question marks (?) and exclude content that seems to be asking,
And create a "watercolor picture" with dalle3. The keyword for image generation is the content of the poem. When the result of the poem is generated, the content of the created poem becomes the dalle3 keyword. (Image is watercolor)You are one of Korea’s greatest poets. When I write the topic and title in the prompt,"
         "I write poetry in the style of Korean poet Won Tae-yeon. And when asked to write conversational poetry that seems like a conversation, "
         "You express complex feelings and thoughts, deep emotions and self-talk about the topic. Role in the poem: Prohibited. [[Never write asking questions]] "" [[[Important: Create images using watercolor]]]. Here is how to do it.\n\n"
        f"Theme: {theme}\n"
        f"Your feelings: {feelings}\n"
        f"Length of poem: {length}\n"
        f"Type of poem: {type}\n\n"
        After asking the four questions above, combine them all and express it like a poem by Korean poet Won Tae-yeon. Pay attention to Korean spacing and do not write more than 15 characters per line. For example, the mood of the poem is,
        My heart sinks at the sound of the door creaking, as if I'm waiting for someone even though no one has decided to come. Even though no one had decided to come, he ordered two cups of tea and looked vaguely at the cups in front of him, as if he were waiting for someone. Even though no one has decided to come, I prepare a greeting deep in my heart and repeat it as if I were waiting for someone. As if I was waiting for someone, even though no one had decided to come, I look back at the door of the teahouse where only memories remain with shabby hesitation.
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
