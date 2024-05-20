import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)


review_template_str = """Your job is to use Google Maps
reviews to summarize all of the given interviews as well as provide
key features of the place with one or two words (positive, negative and neutral). Please, provide the output in a JSON format
with the following keys:
summary, positive_features, negative_features, neutral_features

If the features are longer than 2 words, shorten them to two words. 
For example: positive feature is "wide drinks selection" shorten it to "drinks selection".
"""

class ChatBot:
    def __init__(self):
        review_system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],
                template=review_template_str,
            )
        )

        review_human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["question"],
                template="{question}",
            )
        )
        messages = [review_system_prompt, review_human_prompt]

        review_prompt_template = ChatPromptTemplate(
            input_variables=["question"],
            messages=messages,
        )

        chat_model = ChatOpenAI(model="gpt-4o-2024-05-13", temperature=0)

        review_chain = review_prompt_template | chat_model

        self.review_chain = review_chain

    def call_chat(self, question):
        return self.review_chain.invoke({"question": question})