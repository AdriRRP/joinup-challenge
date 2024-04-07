// Create a new database and switch to it
db = db.getSiblingDB('challenge');

// Create a user with read and write privileges for the database
db.createUser({
    user: 'user_admin',
    pwd: 'us3r_4dm1n',
    roles: [
        {
            role: 'readWrite',
            db: 'challenge',
        },
    ],
});