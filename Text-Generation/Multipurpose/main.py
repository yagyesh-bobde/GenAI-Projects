# Import Required Packages
import streamlit as st
import google.generativeai as genai

# Define some variables already to avoid errors
mailtype=""
Reply=""
optionpg1=""

# Sidebar code
with st.sidebar:
    # Here we take Gemini API as a Input from user
    api_key = st.text_input("API Key", type="password")
    st.markdown("[Get Your API Key](https://makersuite.google.com/app/apikey)")

    # Select the type of Text Generation
    option = st.selectbox(
    'Select type of app you want?',
    ('Text Generation', 'Email Generation', 'Post Generation','Essay Generation'))

    # If we select Post Generation Option
    if(option=="Post Generation"):
       optionpg1 = st.selectbox('Choose Social Media',('Linkedin','Twitter/X'))

        # In Post Generation , we select Linkedin  
       if(optionpg1=="Linkedin"):
          style = st.selectbox('Choose Post Style',('Professional','Friendly','Creative','Inspirational','Storytelling'))
          domain = st.text_input('Your Working Domain/Field')
          optionlp = st.selectbox('Select length of post you want?',('small -  approx 150 words', 'medium -  approx 350 words', 'long -  approx 500 words'))

        # In Post Generation , we select twitter
       if(optionpg1=="Twitter/X"):
          style1 = st.selectbox('Choose Post Style',('Professional','Friendly','Creative','Inspirational','Storytelling'))
          optiontp = st.selectbox('Select length of post you want?',('small -  approx 50 words', 'medium -  approx 150 words', 'long -  approx 250 words'))

    #  If we select Eassy Generation Option
    if(option=="Essay Generation"):
        optioneg1 = st.selectbox(
        'Select length of essay you want?',
        ('small -  approx 150 words', 'medium -  approx 350 words', 'long -  approx 500 words','extensive -  more than 800 words'))
        
    
    if(option=="Essay Generation"):
         optioneg2 = st.selectbox(
        'Select type of essay you want?',
        ('simple', 'descriptive', 'narrative','Persuasive','professional'))

    # If we select Email Generation Option
    if(option=="Email Generation"):
        mailtype = st.radio(
        "Select Email Type 👇",
        ["Compose", "Reply"],
        horizontal=True,
        )

        # If we want to Compose mail
        if(mailtype=="Compose"):
            sender=st.text_input("Name of sender with details")
            receiver=st.text_input("Name of receiver with details")
            optionec1 = st.selectbox(
            'Select length of essay you want?',
            ('small -  approx 150 words', 'medium -  approx 350 words', 'long -  approx 500 words','extensive -  more than 800 words'),index=1)

            emailtone = st.selectbox(
            'Select tone of essay you want?',
            ('Friendly', ' Funny', 'Casual','Excited','Professional','Sarcastic','Persuasive'),index=0)

            emaillang = st.selectbox(
            'Select tone of essay you want?',
            ("Arabic", "Bengali", "Bulgarian", "Chinese simplified", "Chinese traditional", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese", "Korean", "Latvian", "Lithuanian", "Norwegian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Thai", "Turkish", "Ukrainian", "Vietnamese"),index=9)

        # IF we want to reply some mail
        if(mailtype=="Reply"):
            sender1=st.text_input("Name of sender with details")
            receiver1=st.text_input("Name of receiver with details")
            optionec2 = st.selectbox(
            'Select length of essay you want?',
            ('small -  approx 150 words', 'medium -  approx 350 words', 'long -  approx 500 words','extensive -  more than 800 words'),index=1)

            emailtone1 = st.selectbox(
            'Select tone of essay you want?',
            ('Friendly', ' Funny', 'Casual','Excited','Professional','Sarcastic','Persuasive'),index=0)

            emaillang1 = st.selectbox(
            'Select tone of essay you want?',
            ("Arabic", "Bengali", "Bulgarian", "Chinese simplified", "Chinese traditional", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese", "Korean", "Latvian", "Lithuanian", "Norwegian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Thai", "Turkish", "Ukrainian", "Vietnamese"),index=9)

    st.header('About Me')
    st.markdown("[Linkedin](https://www.linkedin.com/in/sanketshinde04/)")
    st.markdown("[Github](https://github.com/sanketshinde3001)")

# Heading Changes as per our Choices
st.title(option)    

# Here we Configure api
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')    

# Funtion used to get output
def generate(prompt):
    response = model.generate_content(prompt)
    return response

# If we select Essay Generation
if(option=="Essay Generation"):
 with st.form("myform"):
    ip=st.text_input("Write topic of essay")
    additional=st.text_input("Write some extra about topic (optional)")

    submitted = st.form_submit_button("Submit")

    prompt = f"""Write an essay that is on topic - {ip} with a {optioneg1} tone. Here are some additional points regarding this -  {additional}. Structure your essay with a clear introduction, body paragraphs that support your thesis, and a strong conclusion. Use evidence and examples to illustrate your points. Ensure your writing is clear, concise, and engaging.Pay attention to tone given above , grammar, spelling, and punctuation. Most importent give me essay {option} long """
    
    if not api_key:
        st.info("Please add your API key to continue.")
    elif submitted:
        response=generate(prompt)
        # st.write(prompt)
        st.write(response.text)

# If we select Text Generation
if(option=="Text Generation"):
 with st.form("myform"):
    ip=st.text_input("Enter whatever you want to enter..")
    # st.caption('For eg - Indian , Street Food , Chinease')

    submitted = st.form_submit_button("Submit")

    prompt=ip

    if not api_key:
        st.info("Please add your API key to continue.")
    elif submitted:
        response=generate(prompt)
        # st.write(prompt)
        st.write(response.text)


# If we want to compose a mail
if(mailtype=="Compose"):
 with st.form("myformcompose"):
    subject=st.text_input("Subject of Email")
    Purpose=st.text_input("Purpose of Email")
    # st.caption('For eg - Indian , Street Food , Chinease')

    submitted = st.form_submit_button("Submit")

    prompt = f"""Compose a professional email with a tone appropriate for the purpose of {Purpose}. **To:** {receiver} **From:** {sender}**Subject:** {subject}
    **Body:**
    Begin the email with a friendly and appropriate greeting, addressing the recipient by name.
    Clearly state the purpose of the email in the first sentence or two.
    Provide concise and relevant information related to the purpose, using a clear and easy-to-read format.
    Structure the body paragraphs logically, using bullet points or numbered lists if necessary.
    Very important Maintain a {emailtone} throughout the email.
    **Closing:**
    End the email with a polite closing phrase, such as "Sincerely," "Best regards," or "Thank you."
    Include the sender's full name and contact information (email address, phone number, etc.) below the closing.
    **Additional details:**
    - Proofread the email carefully before sending to ensure accuracy and clarity.
    - The email length must be {optionec1} and give me in language {emaillang}"""
    
    if not api_key:
        st.info("Please add your API key to continue.")
    elif submitted:
        response=generate(prompt)
        # st.write(prompt)
        st.write(response.text)

# If we want to generate reply to the mail
if(mailtype=="Reply"):
 with st.form("myformreply"):
    replyto = st.text_area("Received Mail")
    subject1=st.text_input("Subject of Email")
    Purpose1=st.text_input("Purpose of Email")
    # st.caption('For eg - Indian , Street Food , Chinease')

    submitted = st.form_submit_button("Submit")

    prompt = f"""**Analyze the following email received from {receiver1} and generate a suitable response for {sender1}:**
    **Subject:** {subject1}
    **Body:**{replyto}
    **Context and Purpose:**
    * **Purpose of the email:** {Purpose1}
    * **Desired tone of the reply:** {emailtone1}
    **Specific Points and Instructions:**
    * **Key issues or requests raised by the sender:** Briefly summarize the main points the sender wants to address.
    * **Specific questions to answer:** List any specific questions you need to answer in the reply.
    * **Desired action or outcome:** What do you want to achieve with your reply? (e.g., Schedule a meeting, provide information, address concerns)
    **Reply Generation:**
    * **Generate a reply that is:**
        * Clear, concise, and {emailtone1} tone
        * Start the email with polite phrase as per post of receiver (eg. Respected , Dear , etc)
        * Consistent with the tone of the original email
        * Addresses the sender's concerns or requests
        * Takes the appropriate action based on the purpose of the email
        **I look forward to assisting you in crafting the perfect email response in language {emaillang1} and reply must have length {optionec2}!** """
    
    if not api_key:
        st.info("Please add your API key to continue.")
    elif submitted:
        response=generate(prompt)
        # st.write(prompt)
        st.write(response.text)

# If we want to make linkedin Post
if(optionpg1=="Linkedin"):
 with st.form("myformlinkedin"):
    desc = st.text_area("Describe About Post")

    submitted = st.form_submit_button("Submit")

    prompt = f"""**Craft a LinkedIn post that captures attention and sparks conversations.**
    **Imagine you're a skilled storyteller, weaving a captivating narrative that blends:**
    - A {style} tone, resonating with your audience's emotions and values.
    - A length of approximately {optionlp} words, delivering your message concisely and impactfully.
    - I work is related to domain of {domain}.
    - These key elements, handpicked to shape your story:{desc}

**Guidelines for your masterpiece:**

- **Paint a vivid picture:** Use descriptive language and maintain post tone like {style}.
- **Add Emoji to make post more attractive
- **Weave in relevant keywords and hashtags:** Enhance visibility and reach within your professional network.
- **Polish your prose to perfection:** Ensure clarity, conciseness, and flawless grammar.
**Now, Bard, unleash your creativity and craft a LinkedIn post that resonates, inspires, and leaves a lasting impression!**"""
    
    if not api_key:
        st.info("Please add your API key to continue.")
    elif submitted:
        response=generate(prompt)
        # st.write(prompt)
        st.write(response.text)

# If we want to generate tweet
if(optionpg1=="Twitter/X"):
 with st.form("myformtwitter"):
    desc1 = st.text_area("Describe About Post")
    submitted = st.form_submit_button("Submit")

    prompt = f"""Prompt for generating Twitter posts that capture human-like creativity and authenticity.
    Template:
    Write a tweet that is {style1} in tone, {optiontp} characters long, and incorporates the following elements:
    * {desc1}
    Ensure the tweet is:
    * Engaging and attention-grabbing
    * Clear and concise
    * Likely to resonate with their audience
    * Add Mentions if possible and must add tags at end
    Feel free to use creative language, wordplay, humor, or other techniques to make the tweet stand out.
    """
    
    if not api_key:
        st.info("Please add your API key to continue.")
    elif submitted:
        response=generate(prompt)
        # st.write(prompt)
        st.write(response.text)

# to hide made with streamlit part
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0e1117;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/sanketshinde04/" target="_blank">Sanket Shinde</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
