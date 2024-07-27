from abc import ABC, abstractmethod

from base import BACKEND_LOGGER
from base.constants import TEXT_LENGTH_THRESHOLD
from base.enums import ContractType
from base.prompts import (CONTRACT_INFO_EXTRACTION, CONTRACT_TEMPLATE,
                          REVENUE_LEAKAGE_POINTS)
from backend.utils import (AzureOpenAIAssistant, CustomValidation,
                                    UtilityFunctions)


class SummarizationStrategy(ABC):
    @abstractmethod
    def summarize(self, text: str) -> str:
        """
        Summarize the given text.

        Args:
            text (str): The text to be summarized.

        Returns:
            str: The summarized text.
        """
        pass


class LargeContractSummarization(SummarizationStrategy):
    def __init__(self) -> None:
        self.thread_id = None
        self.gpt_obj = None

    def summarize_chunk(self, chunk: str) -> str:
        """
        Summarize a chunk of text.

        Args:
            chunk (str): A chunk of text to be summarized.

        Returns:
            str: The summarized text.
        """
        try:
            prompt = f"Provide a clear and concise summary of the following text: {chunk}"

            if self.thread_id is None:
                gpt_response = self.gpt_obj.first_conversation(
                    user_query=prompt)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for first conversation")
                self.thread_id = gpt_response['thread_id']

            else:
                gpt_response = self.gpt_obj.next_conversion(
                    user_query=prompt, thread_id=self.thread_id)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")

            return gpt_response['response']

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during Large Contract Chunk Summarization: {str(e)}")
            raise CustomValidation()

    def summarize(self, pdf_text: str, gpt_obj: AzureOpenAIAssistant) -> str:
        """
        Summarize a large contract.

        Args:
            pdf_text (str): The text of the large contract to be summarized.

        Returns:
            str: The summarized text.
        """
        try:
            self.gpt_obj = gpt_obj

            BACKEND_LOGGER.info("Inside Large Contract Summarization")
            chunks = UtilityFunctions.split_text_into_chunks(pdf_text)
            summaries = [self.summarize_chunk(chunk) for chunk in chunks]
            combined_summary = ' '.join(summaries)
            return combined_summary, self.thread_id

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during Large Contract Summarization: {str(e)}")
            raise CustomValidation()


class SmallContractSummarizationEngine(SummarizationStrategy):
    def summarize(self, pdf_text: str, gpt_obj: AzureOpenAIAssistant) -> str:
        """
        Summarize a small contract.

        Args:
            pdf_text (str): The text of the small contract to be summarized.

        Returns:
            str: The summarized text.
        """
        try:
            BACKEND_LOGGER.info("Inside Small Contract Summarization")
            prompt = f"Provide clear and concise summary of {pdf_text} explaining the important dates, payment details \
                and contract details"

            gpt_response = gpt_obj.first_conversation(user_query=prompt)

            if not gpt_response["status"]:
                raise CustomValidation(
                    "Failed to generate response from Azure GPT Assitant for first conversation")

            return gpt_response['response'], gpt_response['thread_id']

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during Small Contract Summarization: {str(e)}")
            raise CustomValidation()


class ContractSummarizationEngine:
    def __init__(self, strategy: SummarizationStrategy = None):
        """
        Initialize the ContractSummarizationEngine with a strategy.

        Args:
            strategy (SummarizationStrategy, optional): The summarization strategy to use. Defaults to None.
        """
        self.strategy = strategy

    def set_strategy(self, strategy: SummarizationStrategy):
        """
        Set the summarization strategy.

        Args:
            strategy (SummarizationStrategy): The summarization strategy to set.
        """
        self.strategy = strategy

    def summarize_contract(self, pdf_text: str, gpt_object: AzureOpenAIAssistant) -> str:
        """
        Summarize the contract based on the chosen strategy.

        Args:
            pdf_text (str): The text of the contract to be summarized.

        Returns:
            str: The summarized contract.
        """
        return self.strategy.summarize(pdf_text, gpt_object)

    def determine_strategy(self, pdf_text: str) -> SummarizationStrategy:
        """
        Determine the appropriate strategy based on the length of the contract.

        Args:
            pdf_text (str): The text of the contract.

        Returns:
            SummarizationStrategy: The determined summarization strategy.
        """
        try:
            if len(pdf_text.split()) > TEXT_LENGTH_THRESHOLD:
                return LargeContractSummarization()
            else:
                return SmallContractSummarizationEngine()

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while determining contract summarization strategy: {str(e)}")
            raise CustomValidation()

    def generate_result(self, data: dict) -> str:
        """
        Generate the summarized contract.

        Args:
            data (dict): Dictionary containing the contract data.

        Returns:
            str: The summarized contract.
        """
        try:
            thread_id = data.get('thread_id')
            user_query = data.get('user_query')
            base64_string = data.get('contract_pdf')
            gpt_obj = AzureOpenAIAssistant()

            if base64_string:
                pdf_text = UtilityFunctions.get_pdf_content(base64_string)
                self.set_strategy(self.determine_strategy(pdf_text))
                summarized_contract, thread_id = self.summarize_contract(
                    pdf_text, gpt_obj)
                return {"response": summarized_contract, "thread_id": thread_id}

            else:
                gpt_response = gpt_obj.next_conversion(
                    user_prompt=user_query, thread_id=thread_id)
                if not gpt_response['status']:
                    raise CustomValidation(
                        message="Failed to generate response from Azure GPT Assitant for after first conversation")

                return {"response": gpt_response['response'], "thread_id": gpt_response['thread_id']}

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while preparing response of Contract Summarization: {str(e)}")
            raise CustomValidation()


class ContractStandardComparisonEngine:
    def __init__(self) -> None:
        self.thread_id = None
        self.gpt_obj = AzureOpenAIAssistant()

    def make_conversation_from_gpt(self, prompt):
        try:
            if self.thread_id is None:
                BACKEND_LOGGER.info("first conversion..................")
                gpt_response = self.gpt_obj.first_conversation(
                    user_query=prompt)
            else:
                BACKEND_LOGGER.info("next conversion..............")
                gpt_response = self.gpt_obj.next_conversion(
                    user_prompt=prompt, thread_id=self.thread_id)

            if not gpt_response["status"]:
                raise CustomValidation(
                    "Failed to extract contract details from Azure GPT Assitant for after first conversation")
            self.thread_id = gpt_response['thread_id']
            return gpt_response['response']
        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during contract details extraction in Contract Standard Comparison: {str(e)}")
            raise CustomValidation(
                "An error occurred during contract details extraction in Contract Standard Comparison.")

    def extract_contract_deatils(self, contract_text_list):
        try:
            result = [self.make_conversation_from_gpt(prompt=CONTRACT_INFO_EXTRACTION.format(
                contract_chuncked_text=chuck)) for chuck in contract_text_list]
            return " ".join(result)

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during contract details extraction in Contract Standard Comparison: {str(e)}")
            raise CustomValidation(
                "An error occurred during contract details extraction in Contract Standard Comparison.")

    def compare_standards(self, contract_standards: str, master_contract_standards: str) -> str:
        """
        Compare the standards of a contract with the master contract standards.

        Args:
            contract_standards (str): Standards identified from the contract.
            master_contract_standards (str): Standards identified from the master contract.

        Raises:
            CustomValidation: If there's a failure in generating the GPT response.

        Returns:
            str: Comparison result.
        """
        try:
            prompt = f"Compare the {contract_standards} standards with the {master_contract_standards} standards."

            return self.make_conversation_from_gpt(prompt=prompt)

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during standard comparison of Contract Standard Comparison: {str(e)}")
            raise CustomValidation(
                "An error occurred during standard comparison.")

    def generate_result(self, data: dict) -> str:
        """
        Generate a result by comparing the standards of a contract with master contract standards.

        Args:
            data (dict): Dictionary containing the base64-encoded PDF of the contract.

        Raises:
            CustomValidation: If there's a failure in PDF content extraction or standard comparison.

        Returns:
            str: Comparison result.
        """
        try:
            base_base64_string = data.get("contract_pdf")
            master_base64_string = data.get("master_contract_pdf")
            user_query = data.get("user_query")
            thread_id = data.get("thread_id")

            if base_base64_string and master_base64_string:
                base_pdf_text = UtilityFunctions.get_pdf_content(
                    base_base64_string)
                master_pdf_text = UtilityFunctions.get_pdf_content(
                    master_base64_string)
                base_contract_info = UtilityFunctions.split_text_into_chunks_using_model(
                    base_pdf_text, chunk_size=5000)
                master_contract_info = UtilityFunctions.split_text_into_chunks_using_model(
                    master_pdf_text, chunk_size=5000)
                base_contract_details = self.extract_contract_deatils(
                    base_contract_info)
                master_contract_details = self.extract_contract_deatils(
                    master_contract_info)

                comparison_result = self.compare_standards(
                    base_contract_details, master_contract_details)

                return {"response": comparison_result, "thread_id": self.thread_id}

            else:
                gpt_response = self.gpt_obj.next_conversion(
                    user_prompt=user_query, thread_id=thread_id)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")

                return {"response": gpt_response['response'], "thread_id": gpt_response['thread_id']}

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while preparing response for Contract Standard Comparison: {str(e)}")
            raise CustomValidation()


class ContractAuthoringStrategy(ABC):
    @abstractmethod
    def generate_contract_template(self, standards: str) -> str:
        """Generate a contract template based on provided standards.

        Args:
            standards (str): The standards or guidelines to be incorporated into the contract template.

        Returns:
            str: The generated contract template.
        """
        pass

    @abstractmethod
    def generate_contract(self, **kwargs) -> str:
        """Generate a full contract based on the specific contract authoring strategy.

        Returns:
            str: The generated contract.
        """
        pass


class CustomContractAuthoring(ContractAuthoringStrategy):
    def __init__(self) -> None:
        self.gpt_obj = None

    def generate_contract_template(self, user_prompt: str) -> str:
        """Generate a custom contract template based on user input.

        Args:
            user_prompt (str): The user-provided input for the contract template.

        Returns:
            str: The generated custom contract template.
        """
        try:
            prompt = f"""Based on the provided input: {user_prompt}, generate a contract agreement.
            Use the following template as a structure example but ensure to incorporate the input appropriately:
            {CONTRACT_TEMPLATE}"""

            gpt_response = self.gpt_obj.first_conversation(
                user_query=prompt)
            if not gpt_response["status"]:
                raise CustomValidation(
                    "Failed to generate response from Azure GPT Assitant for first conversation")

            return gpt_response['response'], gpt_response['thread_id']

        except CustomValidation as exc:
            raise exc
        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during custom contract generation: {str(e)}")
            raise CustomValidation()

    def generate_contract(self, gpt_obj: AzureOpenAIAssistant, **kwargs) -> str:
        """Generate a full custom contract based on user input.

        Returns:
            str: The generated custom contract.
        """
        try:
            BACKEND_LOGGER.info("Generating Custom Contract")
            self.gpt_obj = gpt_obj
            user_prompt = kwargs.get('user_prompt')
            return self.generate_contract_template(user_prompt)
        except CustomValidation as exc:
            raise exc
        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred during custom contract generation: {str(e)}")
            raise CustomValidation()


class ContractAuthoringEngine:
    def __init__(self):
        """Initialize the ContractAuthoringEngine with available contract authoring strategies."""
        self.strategies = {
            ContractType.CUSTOM.value: CustomContractAuthoring()
        }

    def generate_contract(self, contract_type: str, gpt_obj: AzureOpenAIAssistant,  **kwargs) -> str:
        """Generate a contract based on the specified contract type.

        Args:
            contract_type (str): The type of contract to generate.

        Raises:
            CustomValidation: If the contract type is unsupported.

        Returns:
            str: The generated contract.
        """
        strategy = self.strategies.get(contract_type)
        if not strategy:
            raise CustomValidation(
                f"Unsupported contract type: {contract_type}")
        return strategy.generate_contract(gpt_obj, **kwargs)

    def generate_result(self, data: dict) -> str:
        """Generate the contract result based on input data.

        Args:
            data (dict): The input data containing contract type and user prompt.

        Raises:
            CustomValidation: If an error occurs during contract generation.

        Returns:
            str: The generated contract result.
        """
        try:
            BACKEND_LOGGER.info("Generating contract result")
            thread_id = data.get('thread_id')
            user_query = data.get('user_query')
            contract_type = data.get("contract_type")
            user_prompt = data.get("user_prompt")
            gpt_obj = AzureOpenAIAssistant()

            if contract_type:
                generated_contract, thread_id = self.generate_contract(
                    contract_type, gpt_obj, user_prompt=user_prompt)
                return {"response": generated_contract, "thread_id": thread_id}

            else:
                gpt_response = gpt_obj.next_conversion(
                    user_prompt=user_query, thread_id=thread_id)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")

                return {"response": gpt_response['response'], "thread_id": gpt_response['thread_id']}

        except CustomValidation as exc:
            raise exc
        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while generating contract result: {str(e)}")
            raise CustomValidation()


class ContractSpendAnalyticsEngine:
    def __init__(self) -> None:
        self.thread_id = None
        self.gpt_obj = AzureOpenAIAssistant()

    def identify_revenue_leakage(self, chunk: str) -> str:
        """
        Identify potential revenue leakages in a text chunk.

        Args:
            chunk (str): A chunk of text from the document to analyze.

        Raises:
            CustomValidation: If the GPT response generation fails.
            CustomValidation: If any other exception occurs.

        Returns:
            str: GPT response containing potential revenue leakages.
        """
        try:
            prompt = f"Identify the potential revenue leakages in the {chunk} by referring to \
                the {REVENUE_LEAKAGE_POINTS}"

            if self.thread_id is None:
                gpt_response = self.gpt_obj.first_conversation(
                    user_query=prompt)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for first conversation")

                self.thread_id = gpt_response['thread_id']

            else:
                gpt_response = self.gpt_obj.next_conversion(
                    user_prompt=prompt, thread_id=self.thread_id)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")

            return gpt_response['response']

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred in identify_revenue_leakage of Contract Spend Analytics: {str(e)}")
            raise CustomValidation()

    def summarize_document(self, document: str) -> str:
        """
        Summarize the entire document by analyzing chunks for revenue leakage.

        Args:
            document (str): The full text of the document to summarize.

        Raises:
            CustomValidation: If the revenue leakage identification fails.
            CustomValidation: If any other exception occurs.

        Returns:
            str: Combined summary of potential revenue leakages in the document.
        """
        try:
            chunks = UtilityFunctions.split_text_into_chunks(document)
            summaries = [self.identify_revenue_leakage(
                chunk) for chunk in chunks]
            combined_summary = ' '.join(summaries)
            return combined_summary

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while summarizing the document in Contract Spend Analytics: {str(e)}")
            raise CustomValidation()

    def generate_result(self, data: dict) -> str:
        """
        Generate a result by analyzing the contract PDF for revenue leakages.

        Args:
            data (dict): Dictionary containing the base64-encoded PDF.

        Raises:
            CustomValidation: If the PDF content extraction or summarization fails.
            CustomValidation: If any other exception occurs.

        Returns:
            str: Summary of potential revenue leakages in the contract PDF.
        """
        try:
            BACKEND_LOGGER.info("Inside Contract Spend Analytics")

            base64_string = data.get("contract_pdf")
            user_query = data.get("user_query")
            thread_id = data.get("thread_id")
            if base64_string:
                pdf_text = UtilityFunctions.get_pdf_content(base64_string)

                contract_analysis = self.summarize_document(pdf_text)
                return {"response": contract_analysis, "thread_id": self.thread_id}

            else:
                gpt_response = self.gpt_obj.next_conversion(
                    user_prompt=user_query, thread_id=thread_id)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")

                return {"response": gpt_response['response'], "thread_id": gpt_response['thread_id']}

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while preparing response for Contract Spend Analytics: {str(e)}")
            raise CustomValidation()


class SimpleContractConversationalEngine:
    def __init__(self) -> None:
        self.thread_id = None
        self.gpt_obj = AzureOpenAIAssistant()

    def generate_result(self, data: dict) -> str:
        try:
            BACKEND_LOGGER.info("Inside Simple Contract Conversation")

            base64_string = data.get("contract_pdf")
            user_query = data.get("user_query")
            thread_id = data.get("thread_id")
            if base64_string:
                pdf_text = UtilityFunctions.get_pdf_content(base64_string)
                prompt = f"Analysis the passed contract, provide the response of user query based on passed contract \
                    text. CONTRACT TEXT : {pdf_text}"
                gpt_response = self.gpt_obj.first_conversation(
                    user_query=prompt)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")
                self.thread_id = gpt_response['thread_id']
                return {"response": gpt_response['response'], "thread_id": self.thread_id}

            else:
                gpt_response = self.gpt_obj.next_conversion(
                    user_prompt=user_query, thread_id=thread_id)
                if not gpt_response["status"]:
                    raise CustomValidation(
                        "Failed to generate response from Azure GPT Assitant for after first conversation")

                return {"response": gpt_response['response'], "thread_id": gpt_response['thread_id']}

        except CustomValidation as exc:
            raise exc

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred while preparing response for Contract Spend Analytics: {str(e)}")
            raise CustomValidation()
