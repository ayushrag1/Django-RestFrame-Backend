import base64
import io

import PyPDF2
import PyPDF2.errors
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers

from base import BACKEND_LOGGER
from base.enums import ContractType


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf', 'txt']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))
        except PyPDF2.errors.PdfReadError as e:
            BACKEND_LOGGER.warning(e)
        else:
            return 'pdf'

    def to_representation(self, value):
        # Convert file to base64
        if not value:
            return None
        with value.open('rb') as file:
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode('utf-8')
            return base64_encoded


class ContractSummarizationSerializer(serializers.Serializer):
    contract_pdf = PDFBase64File(required=False)
    thread_id = serializers.CharField(required=False)
    user_query = serializers.CharField(required=False)

    def validate(self, data):
        thread_id = data.get('thread_id')
        user_query = data.get('user_query')
        contract_pdf = data.get('contract_pdf')

        # Case 1: thread_id and user_query must be provided together
        if thread_id is not None and user_query is None:
            raise serializers.ValidationError(
                "If thread_id is provided, user_query must also be provided.")

        elif thread_id is None and user_query is not None:
            raise serializers.ValidationError(
                "If user_query is provided, thread_id must also be provided.")

        # Case 2: contract_pdf must be provided
        if (not thread_id or not user_query) and not contract_pdf:
            raise serializers.ValidationError(
                "Both thread_id and user_query is required when contract_pdf is not provided.")

        return data


class ContractStandardComparisonSerializer(serializers.Serializer):
    thread_id = serializers.CharField(required=False)
    user_query = serializers.CharField(required=False)
    contract_pdf = PDFBase64File(required=False)
    master_contract_pdf = PDFBase64File(required=False)

    def validate(self, data):
        thread_id = data.get('thread_id')
        user_query = data.get('user_query')
        contract_pdf = data.get('contract_pdf')
        master_contract_pdf = data.get('master_contract_pdf')

        # Case 1: thread_id and user_query must be provided together
        if thread_id is not None and user_query is None:
            raise serializers.ValidationError(
                "If thread_id is provided, user_query must also be provided.")

        elif thread_id is None and user_query is not None:
            raise serializers.ValidationError(
                "If user_query is provided, thread_id must also be provided.")

        # Case 2: contract_pdf must be provided
        if (not thread_id or not user_query) and (not contract_pdf or not master_contract_pdf):
            raise serializers.ValidationError(
                "Both thread_id and user_query is required when contract_pdf or master_contract_pdf is not provided.")

        return data


class ContractAuthoringSerializer(serializers.Serializer):
    thread_id = serializers.CharField(required=False)
    user_query = serializers.CharField(required=False)
    user_prompt = serializers.CharField(required=False)
    contract_type = serializers.ChoiceField(
        choices=tuple(ContractType.value_list()), required=False)

    def validate(self, data):
        thread_id = data.get('thread_id')
        user_query = data.get('user_query')
        user_prompt = data.get('user_prompt')
        contract_type = data.get('contract_type')

        # Case 1: thread_id and user_query must be provided together
        if thread_id is not None and user_query is None:
            raise serializers.ValidationError(
                "If thread_id is provided, user_query must also be provided.")
        elif thread_id is None and user_query is not None:
            raise serializers.ValidationError(
                "If user_query is provided, thread_id must also be provided.")

        # Case 2: contract_type must be provided, and if it's Custom, user_prompt must be provided
        if (thread_id is None or user_query is None) and contract_type is None:
            raise serializers.ValidationError("contract_type is required.")

        elif contract_type == ContractType.CUSTOM.value and user_prompt is None:
            raise serializers.ValidationError(
                "If contract_type is Custom, user_prompt must be provided.")

        return data


class ContractSpendAnalyticsSerializer(serializers.Serializer):
    thread_id = serializers.CharField(required=False)
    user_query = serializers.CharField(required=False)
    contract_pdf = PDFBase64File(required=False)

    def validate(self, data):
        thread_id = data.get('thread_id')
        user_query = data.get('user_query')
        contract_pdf = data.get('contract_pdf')

        # Case 1: thread_id and user_query must be provided together
        if thread_id is not None and user_query is None:
            raise serializers.ValidationError(
                "If thread_id is provided, user_query must also be provided.")

        elif thread_id is None and user_query is not None:
            raise serializers.ValidationError(
                "If user_query is provided, thread_id must also be provided.")

        # Case 2: contract_pdf must be provided
        if (thread_id is None or user_query is None) and contract_pdf is None:
            raise serializers.ValidationError(
                "Both thread_id and user_query is required when contract_pdf is not provided.")

        return data


class ContractConversationalSerializer(serializers.Serializer):
    thread_id = serializers.CharField(required=False)
    user_query = serializers.CharField(required=False)
    contract_pdf = PDFBase64File(required=False)

    def validate(self, data):
        thread_id = data.get('thread_id')
        user_query = data.get('user_query')
        contract_pdf = data.get('contract_pdf')

        # Case 1: thread_id and user_query must be provided together
        if thread_id is not None and user_query is None:
            raise serializers.ValidationError(
                "If thread_id is provided, user_query must also be provided.")

        elif thread_id is None and user_query is not None:
            raise serializers.ValidationError(
                "If user_query is provided, thread_id must also be provided.")

        # Case 2: contract_pdf must be provided
        if (thread_id is None or user_query is None) and contract_pdf is None:
            raise serializers.ValidationError(
                "Both thread_id and user_query is required when contract_pdf is not provided.")

        return data
