# Jormungandr - Onboarding
from .stubs import (
    stub_unique_id,
    stub_mongodb_suitability_template,
    StubPymongoResults,
    stub_customer_answers,
    stub_khonshu_response,
    stub_khonshu_response_failure
)
from func.src.domain.exceptions.repositories.exception import ErrorOnUpdateUser
from func.src.domain.exceptions.services.exception import ErrorCalculatingCustomerSuitability
from func.src.domain.exceptions.transports.exception import InvalidOnboardingCurrentStep
from func.src.services.suitability import SuitabilityService

# Standards
from unittest.mock import patch

# Third party
import pytest
from khonshu import CustomerSuitability


@patch(
    "func.src.services.suitability.UserRepository.update_customer_suitability_data",
    return_value=StubPymongoResults(),
)
@pytest.mark.asyncio
async def test_when_update_customer_suitability_fail_then_raises(mock_update_one):
    with pytest.raises(ErrorOnUpdateUser):
        await SuitabilityService._SuitabilityService__save_customer_suitability_data(
            unique_id=stub_unique_id, suitability=stub_mongodb_suitability_template
        )


@patch(
    "func.src.services.suitability.UserRepository.update_customer_suitability_data",
    return_value=StubPymongoResults(True),
)
@pytest.mark.asyncio
async def test_when_update_customer_suitability_with_success_then_mock_was_called(
    mock_update_one
):
    await SuitabilityService._SuitabilityService__save_customer_suitability_data(
        unique_id=stub_unique_id, suitability=stub_mongodb_suitability_template
    )
    mock_update_one.assert_called_once_with(unique_id=stub_unique_id, suitability=stub_mongodb_suitability_template)


@patch(
    "func.src.services.suitability.UserRepository.update_customer_suitability_data",
    return_value=StubPymongoResults(True),
)
@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_when_update_customer_suitability_with_success_then_return_true(mock_update_one):
    result = await SuitabilityService._SuitabilityService__save_customer_suitability_data(
        unique_id=stub_unique_id, suitability=stub_mongodb_suitability_template
    )

    assert result is True


@patch(
    "func.src.services.suitability.Khonshu.get_suitability_score",
    return_value=stub_khonshu_response,
)
@pytest.mark.asyncio
async def test_when_get_customer_suitability_response_from_khonshu_with_success_then_return_customer_suitability_instance(
    mock_khonshu,
):
    customer_suitability = await SuitabilityService._SuitabilityService__get_customer_suitability_from_khonshu(
        customer_answers=stub_customer_answers
    )

    assert isinstance(customer_suitability, CustomerSuitability)


@patch(
    "func.src.services.suitability.Khonshu.get_suitability_score",
    return_value=stub_khonshu_response,
)
@pytest.mark.asyncio
async def test_when_get_customer_suitability_response_from_khonshu_with_success_then_return_customer_suitability_expeceted_values(
    mock_khonshu,
):
    customer_suitability = await SuitabilityService._SuitabilityService__get_customer_suitability_from_khonshu(
        customer_answers=stub_customer_answers
    )

    assert customer_suitability.profile == 1
    assert customer_suitability.score == 0.6215
    assert customer_suitability.version == 13


@patch(
    "func.src.services.suitability.Khonshu.get_suitability_score",
    return_value=stub_khonshu_response_failure,
)
@pytest.mark.asyncio
async def test_when_get_customer_suitability_from_khonshu_is_not_success_then_raises(
    mock_khonshu,
):
    with pytest.raises(ErrorCalculatingCustomerSuitability):
        await SuitabilityService._SuitabilityService__get_customer_suitability_from_khonshu(
            customer_answers=stub_customer_answers
        )


@patch(
    "func.src.services.suitability.SuitabilityService._SuitabilityService__save_customer_suitability_data"
)
@patch("func.src.services.suitability.Audit.record_message_log")
@patch(
    "func.src.services.suitability.Khonshu.get_suitability_score",
    return_value=stub_khonshu_response,
)
@pytest.mark.asyncio
async def test_when_create_suitability_with_success_then_return_true(
    mock_khonshu_response, mock_audit_response, mock_save_suitability
):
    result = await SuitabilityService.set_in_customer(unique_id=stub_unique_id, customer_answers=stub_customer_answers)

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.suitability.OnboardingSteps.get_user_current_step",
    return_value="suitability",
)
async def test_when_current_step_correct_then_return_true(mock_onboarding_steps):
    result = await SuitabilityService.validate_current_onboarding_step(jwt="123")

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.suitability.OnboardingSteps.get_user_current_step",
    return_value="finished",
)
async def test_when_current_step_invalid_then_return_raises(mock_onboarding_steps):
    with pytest.raises(InvalidOnboardingCurrentStep):
        await SuitabilityService.validate_current_onboarding_step(jwt="123")
