from __future__ import annotations
from typing import Optional

from result import Result, Ok, Err

from app.challenge.config import Config
from lib.challenge.user.domain.user.email import Email
from lib.challenge.user.domain.user.hobbies import Hobbies
from lib.challenge.user.domain.user.id import Id
from lib.challenge.user.domain.user.name import Name
from lib.challenge.user.domain.user.phone import Phone
from lib.challenge.user.domain.user.repository import Repository
from lib.challenge.user.domain.user.surname import Surname
from lib.challenge.user.domain.user.user import User
from lib.challenge.user.domain.user.users import Users

from pymongo import MongoClient
from bson.binary import UUID


class Mongo(Repository):
    """Implementation for mongo challenge repository"""

    def __init__(self, conf: Config):
        """
        This constructor should be private and only called from the new() method.
        This restriction has been omitted for code simplicity.

        @param conf: instance of app configuration
        """

        self._uri = conf.get()['MONGO']['uri']
        self._database_name = conf.get()['MONGO']['database']
        self._collection_name = conf.get()['MONGO']['collection']
        self._user = conf.get()['MONGO']['user']
        self._pass = conf.get()['MONGO']['pass']

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
            found_user = self._collection.find_one({'_id': UUID(id.value())})
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
            return Err(f"Can't find challenge with id `{id.value()}`: {str(e)}")

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
