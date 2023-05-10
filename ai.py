import os
import openai


# This example requires environment variables named "OPEN_AI_KEY" and "OPEN_AI_ENDPOINT"
# Your endpoint should look like the following https://YOUR_OPEN_AI_RESOURCE_NAME.openai.azure.com/
openai.api_key = os.environ.get('OPEN_AI_KEY')
openai.api_base = os.environ.get('OPEN_AI_ENDPOINT')
openai.api_type = 'azure'
openai.api_version = '2022-12-01'
# This will correspond to the custom name you chose for your deployment when you deployed a model.
deployment_id = 'davinci3'


# Prompts Azure OpenAI with a request and synthesizes the response.
async def get_response(prompt):
    # Ask Azure OpenAI
    response = openai.Completion.create(engine=deployment_id, prompt=prompt, max_tokens=100)
    text = response['choices'][0]['text'].replace('\n', ' ').replace(' .', '.').strip()
    print('Azure OpenAI response:' + text)
    return text