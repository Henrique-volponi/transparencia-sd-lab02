def get_user(user_id: int) -> dict:
    return db.query(f"SELECT * FROM users WHERE id={user_id}")

user = get_user(42)
print(user["name"])  
