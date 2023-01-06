from func.src.domain.models.device_info import DeviceInfo
from func.src.domain.suitability.model import SuitabilityModel
from khonshu import CustomerAnswers, CustomerSuitability, KhonshuStatus

stub_unique_id = "db43b7ff-54b2-483c-afab-f686c7eef782"
stub_mongodb_suitability_template = {
    "suitability": {
        "score": 1.0,
        "profile": 4,
        "submission_date": "date",
        "suitability_version": 13,
    }
}


class StubPymongoResults:
    def __init__(self, matched_count: bool = False):
        self.matched_count = matched_count


stub_customer_answers = CustomerAnswers(
    **{
        "answers": [
        ]
    }
)


stub_customer_suitability_calculated = CustomerSuitability(
    profile=1, version=13, score=0.6215
)
stub_device_info = DeviceInfo({"precision": 1}, "")
stub_suitability_model = SuitabilityModel(
    unique_id=stub_unique_id,
    customer_answers=stub_customer_answers,
    customer_suitability=stub_customer_suitability_calculated,
    device_info=stub_device_info,
)

stub_khonshu_response = (
    True,
    KhonshuStatus.SUCCESS,
    stub_customer_suitability_calculated,
)
stub_khonshu_response_failure = (False, KhonshuStatus.INTERNAL_SERVER_ERROR, None)
