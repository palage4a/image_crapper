db.createUser(
    {
        user: "flask",
        pwd: "flask",
        roles: [
            {
                role: "readWrite",
                db: "flask_db"
            }
        ]
    }
);
