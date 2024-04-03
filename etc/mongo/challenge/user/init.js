db = db.getSiblingDB('challenge');
// Create a new collection and insert documents
db.user.insert([
    {
        _id: UUID("d0114468-4c62-4bd1-b128-ca20864876c3"),
        name: "John",
        surname: "Doe",
        email: "john.doe@mail.com",
        phone: "+34 666 666 001",
        hobbies: ["Music", "Cinema"],
        email_verified: true,
        phone_verified: true,
    },
    {
        _id: UUID("757222dd-afd0-4389-a6c2-99e156bed592"),
        name: "Mary",
        surname: "Smith",
        email: "mary.smith@mail.com",
        phone: "+34 666 666 002",
        hobbies: ["Dance", "Sing"],
        email_verified: true,
        phone_verified: true,
    },
]);