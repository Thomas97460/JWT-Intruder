import base64
import sys
import visual
import json
import crypto
import analyzer

class CustomException(Exception):
    pass

def base64_encode_dict(dict) :
    try : 
        dict = json.dumps(dict).replace(" ", "")
        dict = base64.urlsafe_b64encode(dict.encode("utf-8")).decode("utf-8").replace("=","")
        return dict
    except Exception as e :
        print(visual.error("Base64 encode : " + str(e)))
        sys.exit()

def none_algo(token) :
    headers = analyzer.get_header_args(token)
    playload = analyzer.get_playload_64(token)
    signature = analyzer.get_signature_64(token)
    new_headers = {}
    for key, value in headers.items() :
        if(key != "alg") :
            new_headers[key] = value
        else :
            new_headers["alg"] = "none"
    new_headers = base64_encode_dict(new_headers)
    new_token = new_headers + "." + playload + "." + signature
    return new_token

def add_in_playload(args) :
    headers = analyzer.get_header_64(args.token)
    if args.new_playload is not None:
        new_playload = {}
    else :
        new_playload = analyzer.get_playload_args(args.token)
    signature = analyzer.get_signature_64(args.token)
    try :
        if args.new_playload is not None :
            new_args = json.loads(args.new_playload)
        else :
            new_args = json.loads(args.playload)
        for key, value in new_args.items() :
            new_playload[key] = value
    except Exception as e :
        print(visual.error("Argument playload : " + str(e)))
        sys.exit()
    new_playload = base64_encode_dict(new_playload)
    if args.secret_key is not None :
        signature = crypto.sign(args.token, args.secret_key)
    new_token = headers + "." + new_playload + "." + signature
    return new_token

def new_header_64(args) :
    try :
        headers_dict = json.loads(args.head)
        if "typ" in headers_dict :
            del headers_dict["typ"]
        headers_dict["typ"] = "JWT"
    except Exception as e :
        print(visual.error("Bad syntax for headers : " + str(e)))
        sys.exit()
    if not "alg" in headers_dict :
        print(visual.error("ERROR in Header : Need to specify \"alg\":\"your_algorithm\""))
        sys.exit()
    headers_64 = base64_encode_dict(headers_dict)
    return headers_64
    
def new_playload_64(args) :
    try :
        playload_dict = json.loads(args.play)
    except Exception as e :
        print(visual.error("Bad syntax for playload : " + str(e)))
        sys.exit()
    playload_64 = base64_encode_dict(playload_dict)
    return playload_64

def mismatch_header_json(header_json) :
    try : 
        header_dict = json.loads(header_json)
    except Exception as e :
        print(visual.error("Bad header syntax : " + str(e)))
        sys.exit()
    header_dict["alg"] = "HS256"
    try :
        new_header_json =  json.dumps(header_dict).replace(" ", "")
        return new_header_json
    except Exception as e :
        print(visual.error(str(e)))
        sys.exit() 
    