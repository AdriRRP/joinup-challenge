from __future__ import annotations
from typing import Optional

from lib.challenge.email_verification.domain.repository import Repository
from lib.challenge.email_verification.domain.verification import Verification
from lib.shared.domain.value_object.uuid import Uuid
from result import Result, Ok, Err

from app.challenge.config import Config
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.id import Id

from pymongo import MongoClient
from bson.binary import UUID


class Mongo(Repository):
    """Implementation for mongo email verification repository"""

    def __init__(self, conf: Config):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param conf: instance of app configuration
        """

        self._uri = conf.get()['MONGO']['uri']
        self._database_name = conf.get()['MONGO']['database']
        self._user = conf.get()['MONGO']['user']
        self._pass = conf.get()['MONGO']['pass']
        self._collection_name = conf.get()['CHALLENGE']['email_verification_collection']

        self._client = MongoClient(
            self._uri,
            username=self._user,
            password=self._pass,
            authSource=self._database_name,
            authMechanism='SCRAM-SHA-256',
            uuidRepresentation="standard"
        )
        self._database = self._client.get_database(self._database_name)
        self._collection = self._database.get_collection(self._collection_name)

    @staticmethod
    def new(conf: Config) -> Mongo:
        """
        Factory method to create a new mongo challenge Repository object.

        @param conf: instance of app configuration
        @return: new instance of this Mongo repository
        """

        repository = Mongo(conf)
        return repository

    def save(self, verification: Verification):
        self._collection.insert_one({
            '_id': UUID(f"urn:uuid:{verification.code()}"),
            'user_id': UUID(f"urn:uuid:{verification.user_id()}"),
            'email': verification.email(),
            'accepted': False,
        })

    def accept(self, code: Uuid):
        try:
            self._collection.update_one(
                {'_id': UUID(f"urn:uuid:{code.value()}")},
                {"$set": {'accepted': True}}
            )
        except Exception as e:
            # TODO: Manage errors
            print(f"Can't accept email verification with code `{code.value()}`: {str(e)}")

    def find(self, code: Uuid) -> Result[Optional[Verification], str]:
        try:
            found_verification = self._collection.find_one({'_id': UUID(f"urn:uuid:{code.value()}")})
            if found_verification:
                verification = Verification.new(
                    Uuid.new(str(found_verification['_id'])).ok_value,
                    Id.new(str(found_verification['user_id'])).ok_value,
                    Email.new(found_verification['email']).ok_value,
                    str(found_verification['accepted']).lower() == 'true',
                )
                return Ok(verification)
            else:
                return Err(f"Email verification with code `{code.value()}` not found.")
        except Exception as e:
            return Err(f"Can't accept email verification with code `{code.value()}`: {str(e)}")
