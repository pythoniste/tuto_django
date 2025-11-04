import bcrypt

def create_hash(password: str) -> str:
    # Generate a salt
    # rounds defines the cost (work factor), indicating the computational complexity.
    # 12 is typical
    salt = bcrypt.gensalt(rounds=12)

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password.decode()


def convert_hashes_password_to_docker_usage(hashed_password: str) -> str:
    return hashed_password.replace("$", "$$")


def check_hashed_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode(),
    )
