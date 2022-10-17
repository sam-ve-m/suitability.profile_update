# Jormungandr - Onboarding
from ..base_repository.base import MongoDbBaseRepository

# Third party
from decouple import config
from etria_logger import Gladsheim


class SuitabilityRepository(MongoDbBaseRepository):
    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_SUITABILITY_ANSWERS_COLLECTION")]
            return collection
        except Exception as ex:
            Gladsheim.error(
                error=ex, message="Error when trying to get mongo collection"
            )
            raise ex

    @classmethod
    async def find_one_most_recent_suitability_answers(cls) -> dict:
        collection = await cls._get_collection()
        try:
            result = await collection.find_one(
                {"$query": {}, "$orderby": {"$natural": -1}}
            )
            return result
        except Exception as ex:
            message = (
                f"SuitabilityRepository::find_last_suitability_answer:: error on trying to"
                f" get suitability answers"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex
