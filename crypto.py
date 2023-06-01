import analyzer
import visual
import sys
import subprocess
import hmac
import hashlib
import modifier

try :
    import jwt
except Exception as e:
    print(visual.error("You need to install PyJWT module with 'pip install PyJWT' : " + str(e)))
    sys.exit()

class CustomException(Exception):
    pass

def sign(token, filename) :
    try :
        with open(filename, "r") as file :
            key = file.read()
    except Exception as e :
        visual.error(str(e))
        sys.exit()
    header_64 = analyzer.get_header_64(token)
    playload_64 = modifier.get_playload_64(token)
    playload_dict = analyzer.get_playload_args(token)
    data_64 = (header_64 + "." + playload_64).replace("=","")
    algo = analyzer.get_algo(token)
    if algo == "HS256" :
        return sign_hs256(data_64, key)
    elif algo == "HS512" :
        return sign_hs512(data_64, key)
    elif algo == "RS256" :
        return sign_rs256(playload_dict, key)
    elif algo == "RS512" : 
        return sign_rs512(playload_dict, key)
    else :
        visual.error("Algorithms not taken in charge")
        sys.exit()
    
def verify_signature_HMAC_filename(token, filename) :
    try :
        with open(filename, "r") as file :
            key = file.read()
    except Exception as e :
        print(visual.error("Failed opening : " + str(e)))
        sys.exit()
    verify_signature_HMAC(token, key)

def verify_signature_RSA_filename(token, filename) :
    try :
        with open(filename, "r") as file :
            key = file.read()
    except Exception as e :
        print(visual.error("Failed opening : " + str(e)))
        sys.exit()
    verify_signature_RSA(token, key)

def verify_signature_HMAC(token, key) :
    try :
        algo = analyzer.get_algo(token)
        decoded_token = jwt.decode(token, key, algorithms=[analyzer.get_algo(token)])
        print("Signature du token vérifié avec l'algorithme " + analyzer.get_algo(token))
    except Exception as e :
        print(visual.yellow("vérification signature failed : " + str(e)))

def verify_signature_RSA(token, key) :
    try :
        algo = analyzer.get_algo(token)
        decoded_token = jwt.decode(token, key, algorithms=[analyzer.get_algo(token)])
        print("Signature du token vérifié avec l'algorithme " + analyzer.get_algo(token))
    except Exception as e :
        print(visual.yellow("vérification signature failed : " + str(e)))
    
def crack_signature(args) :
    analyzer.is_token_valid(args)
    command = "hashcat -m 16500 " + args.token + " " + args.wordlist
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    exit_code = process.wait()
    output = output.decode("utf-8")
    error = error.decode("utf-8")
    if exit_code == 0 :
        print("Brute Force hashcat terminé")
        if "--show" in output : 
            command += " --show"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            exit_code = process.wait(120)
            output = output.decode("utf-8")
            print(output)
        else :
            print(output)
    else :
        print("Une erreur s'est produite avec hashcat")
        print("Sortie d'erreur du programme Hashcat :")
        print(error, output)

def sign_hs256(data, secret_key) :
    hmac_object = hmac.new(secret_key, data, hashlib.sha256)
    return hmac_object.digest()

def sign_hs512(data, secret_key) :
    hmac_object = hmac.new(secret_key, data, hashlib.sha512)
    return hmac_object.digest()

def sign_rs256(data, private_key, headers={}) : 
    try :
        signature = jwt.encode(data, private_key, headers=headers, algorithm="RS256")
        return signature
    except Exception as e :
        print(visual.error("La clé privé de RSA doit être dans un fichier txt au format pem: " + str(e)))
        sys.exit()

def sign_rs512(data, private_key, headers={}) : 
    try :
        signature = jwt.encode(data, private_key, headers=headers, algorithm="RS512")
        return signature
    except Exception as e :
        print(visual.error("La clé privé de RSA doit être dans un fichier txt au format pem: " + str(e)))
        sys.exit()

def create_token(args) :
    header_64 = modifier.new_header_64(args)
    header_dict = analyzer.get_arguments(analyzer.base64_decode(header_64))
    playload_64 = modifier.new_playload_64(args)
    playload_dict = analyzer.get_arguments(analyzer.base64_decode(playload_64))
    try :
        if header_dict["alg"][0] == "H" :
            with open(args.secret_key, "r") as file :
                secret_key = file.read()
        else :
            with open(args.secret_key, "rb") as file:
                private_key = file.read()
    except Exception as e :
        print(visual.error(str(e)))
        sys.exit()
    data_64 = (header_64 + "." + playload_64).replace("=","")
    if header_dict["alg"] == "HS256" :
        return jwt.encode(playload_dict, secret_key, headers=header_dict, algorithm="HS256")
    elif header_dict["alg"] == "HS512" :
        return jwt.encode(playload_dict, secret_key, headers=header_dict, algorithm="HS256")
    elif header_dict["alg"] == "RS256" :
        token = sign_rs256(playload_dict, private_key, headers=header_dict).replace("=","")
        return token
    elif header_dict["alg"] == "RS512" :
        token = sign_rs512(playload_dict, private_key, headers=header_dict).replace("=","")
        return token
    else :
        print(visual.error("ERROR Algorithm : The specified algorithm is not taken in charge"))
        sys.exit()
