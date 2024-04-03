db = db.getSiblingDB('challenge');
// Create a new collection and insert documents
db.phone_verification.insert([
    {
        _id: UUID("7c01a3c5-c704-448f-9e18-e870a63c7605"),
        user_id: UUID("d0114468-4c62-4bd1-b128-ca20864876c3"),
        phone: "+34 666 666 001",
        accepted: true,
    },
    {
        _id: UUID("52890eed-fb29-4ef4-8b09-0792fda48c7f"),
        user_id: UUID("757222dd-afd0-4389-a6c2-99e156bed592"),
        phone: "+34 666 666 002",
        accepted: true,
    },
]);