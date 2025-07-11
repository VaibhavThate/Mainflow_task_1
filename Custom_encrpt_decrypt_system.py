import numpy as np
import string


# --- Substitution Cipher ---

def generate_substitution_key():
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet[:]
    np.random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled)), dict(zip(shuffled, alphabet))


def substitute_encrypt(message, key):
    message = message.upper()
    return ''.join(key.get(char, char) for char in message)


def substitute_decrypt(cipher, reverse_key):
    return ''.join(reverse_key.get(char, char) for char in cipher)


# --- Matrix Transformation (Hill Cipher inspired) ---

def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))


def create_matrix_key():
    # 2x2 invertible matrix mod 26
    while True:
        matrix = np.random.randint(0, 26, (2, 2))
        if int(round(np.linalg.det(matrix))) % 26 != 0:
            try:
                np.linalg.inv(matrix)  # check if invertible
                return matrix
            except np.linalg.LinAlgError:
                continue


def matrix_encrypt(message, key_matrix):
    message = clean_text(message)
    if len(message) % 2 != 0:
        message += 'X'

    encrypted = ''
    for i in range(0, len(message), 2):
        pair = [ord(c) - ord('A') for c in message[i:i + 2]]
        result = np.dot(key_matrix, pair) % 26
        encrypted += ''.join(chr(int(x) + ord('A')) for x in result)
    return encrypted


def matrix_decrypt(cipher, key_matrix):
    inv_matrix = np.linalg.inv(key_matrix)
    det = int(round(np.linalg.det(key_matrix)))
    inv_det = pow(det, -1, 26)
    adjugate = np.round(inv_matrix * det).astype(int)
    mod_inv_matrix = (inv_det * adjugate) % 26

    decrypted = ''
    for i in range(0, len(cipher), 2):
        pair = [ord(c) - ord('A') for c in cipher[i:i + 2]]
        result = np.dot(mod_inv_matrix, pair) % 26
        decrypted += ''.join(chr(int(x) + ord('A')) for x in result)
    return decrypted


# --- Interface ---

def main():
    print("Custom Encryption Tool")
    print("Choose algorithm:")
    print("1. Substitution Cipher")
    print("2. Matrix Transformation")

    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        key, reverse_key = generate_substitution_key()
        message = input("Enter message to encrypt: ")
        encrypted = substitute_encrypt(message, key)
        decrypted = substitute_decrypt(encrypted, reverse_key)
        print(f"\n[Substitution Cipher]")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")

    elif choice == '2':
        key_matrix = create_matrix_key()
        print(f"Key Matrix:\n{key_matrix}")
        message = input("Enter message to encrypt (letters only): ")
        encrypted = matrix_encrypt(message, key_matrix)
        decrypted = matrix_decrypt(encrypted, key_matrix)
        print(f"\n[Matrix Transformation]")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
