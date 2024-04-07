from __future__ import annotations
from typing import Optional

from result import Result, Ok, Err

from app.challenge.config import Config
from lib.challenge.user.domain.email import Email
from lib.challenge.user.domain.hobbies import Hobbies
from lib.challenge.user.domain.id import Id
from lib.challenge.user.domain.name import Name
from lib.challenge.user.domain.phone import Phone
from lib.challenge.user.domain.repository import Repository
from lib.challenge.user.domain.surname import Surname
from lib.challenge.user.domain.user import User
from lib.challenge.user.domain.users import Users

from pymongo import MongoClient
from bson.binary import UUID


class Mongo(Repository):
    """Implementation for mongo user repository"""

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
        self._collection_name = conf.get()['CHALLENGE']['user_collection']

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

    def find(self, id: Id) -> Result[Optional[User], str]:
        try:
            found_user = self._collection.find_one({'_id': UUID(f"urn:uuid:{id.value()}")})
            if found_user:
                user = User.new(
                    Id.new(str(found_user['_id'])).ok_value,
                    Name.new(found_user['name']).ok_value,
                    Surname.new(found_user['surname']).ok_value,
                    Email.new(found_user['email']).ok_value,
                    Phone.new(found_user['phone']).ok_value,
                    Hobbies.new("\n".join(found_user['hobbies'])),
                    str(found_user['email_verified']).lower() == 'true',
                    str(found_user['phone_verified']).lower() == 'true',
                )
                return Ok(user)
            else:
                return Ok(None)
        except Exception as e:
            return Err(f"Can't find user with id `{id.value()}`: {str(e)}")

    def find_all(self) -> Result[Users, str]:
        try:
            found_users = self._collection.find()
            if found_users.alive:
                users: list[User] = []
                for found_user in found_users:
                    users.append(
                        User.new(
                            Id.new(str(found_user['_id'])).ok_value,
                            Name.new(found_user['name']).ok_value,
                            Surname.new(found_user['surname']).ok_value,
                            Email.new(found_user['email']).ok_value,
                            Phone.new(found_user['phone']).ok_value,
                            Hobbies.new("\n".join(found_user['hobbies'])),
                            str(found_user['email_verified']).lower() == 'true',
                            str(found_user['phone_verified']).lower() == 'true',
                        )
                    )
                return Ok(Users.new(users))
            else:
                return Ok(Users.new([]))
        except Exception as e:
            return Err(f"Can't find all challenge`: {str(e)}")

    def save(self, user: User):
        self._collection.insert_one({
            '_id': UUID(f"urn:uuid:{user.id()}"),
            'name': user.name(),
            'surname': user.surname(),
            'email': user.email(),
            'phone': user.phone(),
            'hobbies': user.hobbies(),
            'email_verified': user.email_verified(),
            'phone_verified': user.phone_verified(),
        })

    def verify_email(self, id: Id):
        try:
            self._collection.update_one(
                {'_id': UUID(f"urn:uuid:{id.value()}")},
                {"$set": {'email_verified': True}}
            )
        except Exception as e:
            # TODO: Manage errors
            print(f"Can't verify email for user with id `{id.value()}`: {str(e)}")

    def verify_phone(self, id: Id):
        try:
            self._collection.update_one(
                {'_id': UUID(f"urn:uuid:{id.value()}")},
                {"$set": {'phone_verified': True}}
            )
        except Exception as e:
            # TODO: Manage errors
            print(f"Can't verify phone for user with id `{id.value()}`: {str(e)}")
