from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from base import BACKEND_LOGGER
from base.utils import (ContractAuthoringEngine, ContractSpendAnalyticsEngine,
                        ContractStandardComparisonEngine,
                        ContractSummarizationEngine,
                        SimpleContractConversationalEngine)
from backend.utils import CustomResponse, CustomValidation

from .serializers import (ContractAuthoringSerializer,
                          ContractConversationalSerializer,
                          ContractSpendAnalyticsSerializer,
                          ContractStandardComparisonSerializer,
                          ContractSummarizationSerializer)


class HealthCheck(APIView):
    def get(self, request):
        BACKEND_LOGGER.info("Entering home page view")
        return CustomResponse(data="Health Check ! True")


class ContractSummarization(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ContractSummarizationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = ContractSummarizationEngine().generate_result(serializer.data)
            return CustomResponse(data=response)

        except CustomValidation as exc:
            raise exc

        except ValidationError as val_error:
            raise val_error

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred at Contract Summarization: {str(e)}")
            raise CustomValidation()


class ContractAuthoring(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ContractAuthoringSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = ContractAuthoringEngine().generate_result(serializer.data)
            return CustomResponse(data=response)

        except CustomValidation as exc:
            raise exc

        except ValidationError as val_error:
            raise val_error

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred at Contract Authoring: {str(e)}")
            raise CustomValidation()


class ContractStandardComparison(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ContractStandardComparisonSerializer(
                data=request.data)
            serializer.is_valid(raise_exception=True)
            response = ContractStandardComparisonEngine().generate_result(serializer.data)
            return CustomResponse(data=response)

        except CustomValidation as exc:
            raise exc

        except ValidationError as val_error:
            raise val_error

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred at Contract Standard Comparison: {str(e)}")
            raise CustomValidation()


class ContractSpendAnalytics(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ContractSpendAnalyticsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = ContractSpendAnalyticsEngine().generate_result(serializer.data)
            return CustomResponse(data=response)

        except CustomValidation as exc:
            raise exc

        except ValidationError as val_error:
            raise val_error

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred at Contract Spend Analytics: {str(e)}")
            raise CustomValidation()


class ContractConversational(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ContractConversationalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            response = SimpleContractConversationalEngine().generate_result(serializer.data)
            return CustomResponse(data=response)

        except CustomValidation as exc:
            raise exc

        except ValidationError as val_error:
            raise val_error

        except Exception as e:
            BACKEND_LOGGER.exception(
                f"Error occurred at Contract Conversational: {str(e)}")
            raise CustomValidation()
