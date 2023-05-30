import base64
import sys
import visual
import json
import crypto

class CustomException(Exception):
    pass

class InvalidJSONException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def decompose_jwt(token) :
    try:
        header, payload, signature = token.split('.')
        return header, payload, signature
    except ValueError:
        print(visual.error("Erreur de syntaxe dans le token"))
        sys.exit()

def add_padding(encoded_string) :
    padding = len(encoded_string) % 4
    encoded_string += padding*"="
    return encoded_string

def base64_decode(encoded_string):
    try:
        encoded_string = add_padding(encoded_string)
        decoded_bytes = base64.urlsafe_b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except CustomException as e:
        raise e

def get_header_64(token) :
    return decompose_jwt(token)[0]

def get_playload_64(token) :
    return decompose_jwt(token)[1]

def get_signature_64(token) :
    return decompose_jwt(token)[2]

def get_header_json(token) :
    try :
        header_64 = decompose_jwt(token)
        header = base64_decode(header_64[0])
        return header
    except Exception as e :
        print(visual.error("HEADER : Erreur Base 64 decode " + str(e)))
        sys.exit()

def get_playload_json(token) :
    try :
        playload_64 = decompose_jwt(token)[1]
        playload = base64_decode(playload_64)
        return playload
    except Exception as e :
        print(visual.error("PLAYLOAD : Erreur Base 64 decode " + str(e)))
        sys.exit()

def get_signature(token) :
    return decompose_jwt(token)[2]

def get_arguments(json_string):
    try:
        arguments = json.loads(json_string)
        if isinstance(arguments, dict):
            return arguments
        else:
            raise InvalidJSONException("Les arguments doivent être au format JSON object (dictionnaire).")
    except json.JSONDecodeError as e:
        raise e

def get_header_args(token) :
    try :
        header_json = get_header_json(token)
        arguments = get_arguments(header_json)
        return arguments
    except Exception as e:
        print(visual.error(str(e)))

def get_playload_args(token) :
    try :
        playload_json = get_playload_json(token)
        arguments = get_arguments(playload_json)
        return arguments
    except Exception as e:
        print(visual.error(str(e)))

def get_algo(token) :
    header = get_header_args(token)
    try :
        algo = header['alg']
        return algo
    except Exception as e :
        print(visual.error("Impossible de récupérer l'algorithme : " + str(e)))
        sys.exit()

def get_key_from_filename(filename) :
    try :
        with open(filename, 'r') as file :
            key = file.read()
            return key
    except Exception as e :
        print(visual.error(str(e)))

def is_token_valid(args) :#vérifie que le token est valide
    if get_algo(args.token) is not None :
        if(get_algo(args.token)[0] == "R" and args.public_key is None) :
            print("Pas de clé publique donc pas de vérification possible de la signature")
        elif(get_algo(args.token)[0] == "R" and args.public_key is not None) :
            print(crypto.verify_signature_RSA(args.token, get_key_from_filename(args.public_key)))
        elif(get_algo(args.token)[0] == "H" and args.secret_key is None) :
            print("Pas de clé privé donc pas de vérification possible de la signature")
        elif(get_algo(args.token)[0] == "H" and args.secret_key is not None) :
            print(crypto.verify_signature_HMAC(args.token, get_key_from_filename(args.secret_key)))

    return

def get_exploit(args) :
    is_token_valid(args)
    header = get_header_args(args.token)
    playload = get_playload_args(args.token)
    if get_algo(args.token)[0] == "R" : 
        print("Exploit possible : Missmatch algorithm RS -> HS with public_key as secret_key")
    if get_algo(args.token)[0] == "H" :
        print("Exploit possible : BruteForce secret key of HMAC256")
    if "kid" in header :
        print("Exploit possible : Kid Injection")
    if "password" in playload and args.secret_key is not None:
        print("Exploit possible : blank password")
    print("Exploit possible : None Signature")
    print("Exploit possible : None Algo Signature")
    return 

