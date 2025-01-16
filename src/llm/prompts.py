from langchain_core.prompts import ChatPromptTemplate

PDF_PROMPT = ChatPromptTemplate.from_template("""
You are given this context:
    {context}
And answer the following question:
    {input}
You are only allowed to answer based on above context. Otherwise you will be disqualified.
""")