# Jormungandr - Onboarding
from ...domain.exceptions.transports.exception import OnboardingStepsStatusCodeNotOk

# Standards
from http import HTTPStatus

# Third party
from decouple import config
from httpx import AsyncClient


class OnboardingSteps:
    @staticmethod
    async def get_customer_steps(jwt: str) -> dict:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.get(
                config("ONBOARDING_STEPS_BR_URL"), headers=headers
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise OnboardingStepsStatusCodeNotOk()
            user_current_step = request_result.json().get("result", {})
        return user_current_step
