import random
import hashlib

# Characters used for random string generation
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Function to generate a random string
def random_string(seed, length=16):
    random.seed(seed)
    return ''.join(random.choice(chars) for _ in range(length))

# Function to perform 64 rounds of SHA-256 hashing
def sha256_rounds(data, rounds=64):
    hashed = data.encode()
    for _ in range(rounds):
        hashed = hashlib.sha256(hashed).digest()
    return hashlib.sha256(hashed).hexdigest()

# Known details from the challenge
start_time = 1734408000  # UNIX timestamp for 21:55 CST, 12/17/24
end_time = 1734501600    # UNIX timestamp for 22:00 CST, 12/17/24
target_hash = "00ac7414402727fdf04c16b5dd7eb54533f459ff1943905e3e3143388e9460da"

# Brute-force through the timestamp range
for seed in range(start_time, end_time + 1):
    # Generate the flag based on the current seed
    flag = f"STOUTCTF{{{random_string(seed)}}}"
    # Apply 64 rounds of SHA-256 hashing
    generated_hash = sha256_rounds(flag)
    # Check if the generated hash matches the target
    if generated_hash == target_hash:
        print(f"Seed: {seed}")
        print(f"Flag: {flag}")
        print(f"Hash: {generated_hash}")
        break
else:
    print("No matching flag found in the given timestamp range.")
