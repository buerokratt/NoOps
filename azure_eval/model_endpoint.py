from typing_extensions import Self
from typing import TypedDict
#from azure.identity import DefaultAzureCredential, get_bearer_token_provider
#from azure.identity import InteractiveBrowserCredential, get_bearer_token_provider
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

from azure.identity import EnvironmentCredential, get_bearer_token_provider

class ModelEndpoint:
    def __init__(self: Self, env: dict) -> None:
        self.env = env
        print(f"self.env: {self.env}")

    class Response(TypedDict):
        query: str
        response: str

    # @trace
    def __call__(self: Self, query: str) -> Response:
        cs_url = "https://cognitiveservices.azure.com/.default"
        
        cred = EnvironmentCredential()
        token = cred.get_token(cs_url)

        print(f"Token length: {len(token.token)} chars; expires_on: {token.expires_on}")

        token_provider = get_bearer_token_provider(
            cred, cs_url
        )

        client = AzureOpenAI(
            azure_endpoint=self.env["azure_endpoint"],
            api_version="2025-01-01-preview",
            azure_ad_token_provider=token_provider,
        )
        # Call the model
        completion = client.chat.completions.create(
            model=self.env["azure_deployment"],
            messages=[
                #{
                #    "role": "system",
                #    "content" : SYSTEM_PROMPT
                #},
                {
                    "role": "user",
                    "content": query,
                }
            ],
            #max_tokens=800,
            #temperature=0.7,
            #top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False,
        )
        output = completion.to_dict()
        return {"query": query, "response": output["choices"][0]["message"]["content"]}