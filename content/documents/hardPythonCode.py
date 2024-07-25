import hashlib
import datetime
import random

def generate_hello_message(seed):
    # Génération d'un hash unique à partir d'une date et d'un seed
    timestamp = int(datetime.datetime.now().timestamp())
    hash_value = hashlib.sha256(f"{timestamp}{seed}".encode()).hexdigest()[:8]
    
    # Conversion du hash en entier et application d'une fonction cryptographique
    integer_hash = int(hash_value, 16)
    encrypted_hello = pow(integer_hash, 3, 257) % 256
    
    # Génération d'une chaîne de caractères aléatoire
    random_string = "".join([chr(random.randint(65, 90)) for _ in range(8)])
    
    # Assemblage du message final
    hello_message = f"Bonjour {random_string}!"
    
    return hello_message

seed = 42  # Vous pouvez changer ce seed pour obtenir un résultat différent
print(generate_hello_message(seed))