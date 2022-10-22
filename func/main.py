# Jormungandr - Onboarding
from src.domain.exceptions.base.base_exceptions import (
    ServiceException,
    RepositoryException,
    TransportException,
    DomainException,
    InternalCode,
)
from src.domain.response.model import ResponseModel
from src.services.jwt import JwtService
from src.services.suitability import SuitabilityService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response
from khonshu import CustomerAnswers
from pydantic import ValidationError


async def update_suitability_profile() -> Response:
    try:
        jwt = request.headers.get("x-thebes-answer")
        raw_customer_answers = request.json
        customer_answers_validated = CustomerAnswers(**raw_customer_answers)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        await SuitabilityService.check_if_able_to_update(jwt=jwt)
        success = await SuitabilityService.set_in_customer(
            unique_id=unique_id, customer_answers=customer_answers_validated
        )
        response = ResponseModel(
            success=success,
            message="Suitability score and profile created successfully",
            code=InternalCode.SUCCESS,
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    except ServiceException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except DomainException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except TransportException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except RepositoryException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except ValidationError as err:
        Gladsheim.error(error=err)
        response = ResponseModel(
            success=False,
            message="Invalid customer answers format",
            code=InternalCode.INVALID_PARAMS,
        ).build_http_response(status_code=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error has occurred",
        ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
