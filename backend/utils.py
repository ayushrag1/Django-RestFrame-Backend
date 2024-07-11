import base64
import os
from datetime import datetime

import fitz
import spacy
import tiktoken
from django.utils.encoding import force_str
from nltk.tokenize import sent_tokenize
from openai import AzureOpenAI, OpenAI
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from base.constants import DEFAULT_ASSITANT_MODEL, MAX_TOKEN

from . import UTILS_LOGGER
from .constants import DATA_FOLDER_PATH


class UtilityFunctions:
    @classmethod
    def pdf_to_base64(cls, pdf_path):
        try:
            with open(pdf_path, "rb") as pdf_file:
                encoded_string = base64.b64encode(
                    pdf_file.read()).decode('utf-8')
            return encoded_string
        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to encode pdf to base64. Reason:{str(e)}")

    @classmethod
    def get_contract_path(cls, filename=None):
        try:
            contract_folder_path = os.path.join(DATA_FOLDER_PATH, "contracts")
            os.makedirs(contract_folder_path, exist_ok=True)
            curr_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{filename}_{curr_datetime}.pdf" if filename else f"{curr_datetime}.pdf"
            file_path = os.path.join(contract_folder_path, filename)
            return file_path
        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to encode pdf to base64. Reason:{str(e)}")

    @classmethod
    def base64_to_pdf(cls, base64_string, output_path):
        try:
            with open(output_path, "wb") as pdf_file:
                pdf_file.write(base64.b64decode(base64_string))
        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to encode pdf to base64. Reason:{str(e)}")

    @classmethod
    def extract_text_from_pdf(cls, pdf_path):
        try:
            text = ""
            document = fitz.open(pdf_path)
            for page_num in range(document.page_count):
                page = document.load_page(page_num)
                text += page.get_text()
            return text
        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to encode pdf to base64. Reason:{str(e)}")

    @classmethod
    def identify_standards(cls, text):
        try:
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(text)

            keywords = ['standards', 'requirements',
                        'specifications', 'scope', 'objectives']

            standards = [sent.text for sent in doc.sents if any(
                keyword in sent.text.lower() for keyword in keywords)]
            return standards
        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to encode pdf to base64. Reason:{str(e)}")

    @classmethod
    def split_text_into_chunks(cls, text, max_tokens=MAX_TOKEN):
        try:
            sentences = sent_tokenize(text)
            chunks = []
            current_chunk = []
            current_length = 0

            for sentence in sentences:
                sentence_length = len(sentence.split())
                if current_length + sentence_length <= max_tokens:
                    current_chunk.append(sentence)
                    current_length += sentence_length
                else:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_length = sentence_length

            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks

        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to split text into chuncks. Reason:{str(e)}")

    @classmethod
    def get_pdf_content(cls, base64_pdf_text):
        try:
            pdf_path = UtilityFunctions.get_contract_path()
            UtilityFunctions.base64_to_pdf(base64_pdf_text, pdf_path)
            pdf_text = UtilityFunctions.extract_text_from_pdf(pdf_path)
            return pdf_text

        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to encode pdf to base64. Reason:{str(e)}")

    @classmethod
    def split_text_into_chunks_using_model(cls, text, chunk_size):
        try:
            # Initialize the tokenizer for the GPT model
            enc = tiktoken.encoding_for_model(
                "gpt-3.5-turbo")  # Adjust model name as needed

            # Tokenize the text
            tokens = enc.encode(text)

            # Split tokens into chunks
            chunks = [tokens[i:i + chunk_size]
                      for i in range(0, len(tokens), chunk_size)]

            # Decode tokens back to text
            chunked_text = [enc.decode(chunk) for chunk in chunks]

            return chunked_text
        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to convert pdf text into its chuncked. Reason:{str(e)}")

    @classmethod
    def get_gpt_response(cls, prompt):
        client = OpenAI(api_key=os.environ.get('OPEN_AI_KEY'))
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.75,
                frequency_penalty=0.0
            )
            return {
                "status": True,
                "response": response.choices[0].message.content.strip(),
                "cost": response.usage.completion_tokens
            }

        except Exception as e:
            UTILS_LOGGER.exception(
                f"Failed to generate response from ChatGPT. Reason:{str(e)}")
            return {
                "status": False,
                "response": str(e)
            }


class AzureOpenAIAssistant:
    def __init__(self) -> None:
        self.gpt_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def create_new_assistant(self, assitant_instruction, assitant_model=DEFAULT_ASSITANT_MODEL):
        assistant = self.gpt_client.beta.assistants.create(
            instructions=assitant_instruction,
            model=assitant_model,
            tools=[]
        )
        return assistant.id

    def first_conversation(self, user_query):
        try:
            thread = self.gpt_client.beta.threads.create(
                messages=[
                    {
                        'role': 'user',
                        'content': user_query
                    }
                ]
            )
            return {"status": True, "thread_id": thread.id, "response": self.run_chat_thread(thread_id=thread.id)}

        except Exception as e:
            UTILS_LOGGER.exception(
                f"An error occured while initiating chat. Reason:{str(e)}")
            return {"status": False, "error_message": str(e)}

    def run_chat_thread(self, thread_id):
        current_chat_thread_run = self.gpt_client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=os.environ.get('ASSISTANT_ID')
        )
        UTILS_LOGGER.info("Chat Running Started......")
        while current_chat_thread_run.status != "completed":
            current_chat_thread_run = self.gpt_client.beta.threads.runs.retrieve(
                run_id=current_chat_thread_run.id, thread_id=thread_id)
            UTILS_LOGGER.info(f"run status:{current_chat_thread_run.status}")
        else:
            UTILS_LOGGER.info("Run Completed")

        messgae_response = self.gpt_client.beta.threads.messages.list(
            thread_id=thread_id).data
        return messgae_response[0].content[0].text.value

    def next_conversion(self, user_prompt, thread_id):
        try:
            # Add a new message to the existing thread
            self.gpt_client.beta.threads.messages.create(thread_id=thread_id,
                                                         role='user',
                                                         content=user_prompt)
            return {"status": True, "thread_id": thread_id, "response": self.run_chat_thread(thread_id=thread_id)}

        except Exception as e:
            UTILS_LOGGER.exception(
                f"An error occured while initiating chat. Reason:{str(e)}")
            return {"status": False, "error_message": str(e)}


class CustomValidation(APIException):
    """
    Custom exception class for validation errors.
    """

    default_message = 'A server error occurred.'

    def __init__(self, message: str = None, details: dict = {},
                 status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                 status: bool = False, cdn_cache_time=None) -> None:
        """
        Initialize the CustomValidationV2 exception.

        Args:
            message (str, optional): The error message to display. Defaults to None.
            details (dict, optional): Additional details about the error. Defaults to {}.
            status_code (int, optional): The HTTP status code to return.
                                        - Defaults to status.HTTP_500_INTERNAL_SERVER_ERROR.
            status (bool, optional): Whether the request was successful or not. Defaults to False.
        """
        self.status = status  # Update status if provided
        self.additional_details = details  # Set additional error details
        self.status_code = status_code  # Set the HTTP status code
        # Update the APIException detail attribute
        self.detail = force_str(message) if message else self.default_message
        self.cdn_cache_time = cdn_cache_time

    def to_dict(self) -> dict:
        """
        Convert the exception to a dictionary representation.

        Returns:
            dict: A dictionary containing the error information.
        """
        return {
            'status': self.status,
            'message': self.detail,
            'data': self.additional_details,
            'status_code': self.status_code
        }


class CustomResponse(Response):
    """A custom response class that provides a standardized format for API responses."""

    def __init__(self, message: str = "Response Generated Successfully", status: bool = True,
                 data: dict = {}, status_code: int = status.HTTP_200_OK):
        """
        Initializes a CustomResponse object.

        Args:
            message (str): The message of the response.
            status (bool, optional): Whether the response is successful. Defaults to True.
            details (dict, optional): Additional details about the response. Defaults to an empty dictionary.
            status_code (int, optional): The HTTP status code of the response. Defaults to 200.
        """
        data = {
            'status': status,
            'message': message,
            'data': data,
            'status_code': status_code
        }
        super().__init__(data=data, status=status_code)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomValidation):
        response.data = exc.to_dict()

    elif response is not None:
        data = {
            'status': False,
            'status_code': response.status_code,
            'message': "Internal Server Error",
            'error': response.data,
        }

        if isinstance(exc, ValidationError):
            data['message'] = "Validation Error"

        else:
            UTILS_LOGGER.info(exc)
            UTILS_LOGGER.info(type(exc))
            UTILS_LOGGER.warning(
                f"Exception: {response.data['detail']} \n",
                exc_info=True
            )

            message = response.data['detail']
            data['message'] = message
            if "detail" in response.data:
                del response.data['detail']

        response.data = data

    else:
        data = {
            'status': False,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': "Failed to Implement Custom Exception Handling",
            'error': str(exc)
        }
        from django.http import JsonResponse
        response = JsonResponse(data, status=500)

    return response
