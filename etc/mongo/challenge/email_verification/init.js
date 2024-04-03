db = db.getSiblingDB('challenge');
// Create a new collection and insert documents
db.email_verification.insert([
    {
        _id: UUID("3ece1fff-0cef-4e5a-9f25-594b0ab015b8"),
        user_id: UUID("d0114468-4c62-4bd1-b128-ca20864876c3"),
        email: "john.doe@mail.com",
        accepted: true,
    },
    {
        _id: UUID("e3c7cab4-8175-4185-a114-4f2667ef0170"),
        user_id: UUID("757222dd-afd0-4389-a6c2-99e156bed592"),
        email: "mary.smith@mail.com",
        accepted: true,
    },
]);