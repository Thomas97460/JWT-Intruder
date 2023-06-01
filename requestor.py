import visual
import sys
import json

try :
    import requests
except Exception as e :
    print(visual.error("You need to install requests module with 'pip install requests' : " + str(e)))
    sys.exit()

def get_headers_dict(args) :
    try :
        with open(args.headers, "r") as file :
            headers_json = file.read()
            headers = json.loads(headers_json)
            return headers
    except Exception as e :
        print(visual.error("HEADERS HTTP : " + str(e)))
        sys.exit()

def set_headers_http(args, new_token) :
    if args.headers is not None :
        headers = get_headers_dict(args)
    else :
        headers = {}
    if args.cookies is not None :
        try : 
            cookies = json.loads(args.cookies)
        except Exception as e :
            print(visual.error("COOKIES HTTP : " + str(e)))
            sys.exit()
    else :
        cookies = {}
    if args.data is not None :
        try :
            data = json.loads(args.data)
        except Exception as e :
            print(visual.error("Data : " + str(e)))
    else :
        data = {}
    cookies["jwt"] = new_token
    headers['Authorization'] = "Bearer " + new_token 
    return {"headers" : headers, "cookies" : cookies, "data" : data}   

def dump_response(response, retour, to_dump) :
    to_dump += (retour + "\n")
    to_dump += (str(response.headers) + "\n")
    to_dump += (response.text)
    to_dump += ("\n\n")
    return to_dump

def analyze_response(args, response, to_dump) :
    retour = ""
    retour_dump = ""
    if response.status_code < 400 :
        retour += "Response [" + visual.green(str(response.status_code)) +"] : "
        retour_dump += "Response [" + str(response.status_code) +"] : "
    else :
        retour += "Response [" + visual.red(str(response.status_code)) +"] : "
        retour_dump += "Response [" + str(response.status_code) +"] : "
    if(args.find is not None) :
        to_find = {}
        try :
            to_find = json.loads(args.find)
        except Exception as e :
            print(visual.error("-find bad syntax, need to be a json list : " + str(e)))
            sys.exit()
        for value in to_find :
            is_found = False
            if value in response.headers :
                retour += visual.green("FOUND:") + value + " in headers "
                retour_dump += "FOUND:" + value + " in headers "
                is_found = True
            if value in response.text :
                retour += visual.green("FOUND:") + value + " in body"
                retour_dump += "FOUND:" + value + " in body"
                is_found = True
            if not is_found :
                retour += visual.red("NOT FOUND:") + value
                retour_dump += "NOT FOUND:" + value
        if args.output is not None :
            to_dump = dump_response(response, retour_dump, to_dump)
            try : 
                with open(args.output, "a") as file :
                    file.write(to_dump)
            except Exception as e :
                print(visual.error("openning output : " + str(e)))
                sys.exit()
    elif args.output is not None :
        to_dump = dump_response(response, retour_dump, to_dump)
        try : 
            with open(args.output, "a") as file :
                file.write(to_dump)
        except Exception as e :
            print(visual.error("openning output : " + str(e)))
            sys.exit()
    print(retour)
    return

def request_get(args, new_token) :
    try :
        http_headers = set_headers_http(args, new_token)
        headers = http_headers["headers"]
        cookies = http_headers["cookies"]
        data = http_headers["data"]
        response = requests.get(args.url, headers=headers, cookies=cookies, data=data)
        print(visual.yellow("Request GET Send"))
        to_dump = "Request => " + str(http_headers) + "\n"
        analyze_response(args, response, to_dump)
    except Exception as e :
        print(visual.error("Request GET : " + str(e)))
        sys.exit()

def request_post(args, new_token) :
    try :
        http_headers = set_headers_http(args, new_token)
        headers = http_headers["headers"]
        cookies = http_headers["cookies"]
        data = http_headers["data"]
        request = requests.Request('POST', args.url, headers=headers, cookies=cookies, data=data)
        print('Request URL:', request.url)
        print('Request Method:', request.method)
        print('Request Headers:', request.headers)
        print('Request Cookies:', request.cookies)
        print('Request Data:', request.data)
        response = requests.Session().send(request.prepare())
        # response = requests.post(args.url, headers=headers, cookies=cookies, data=data)
        print(visual.yellow("Request POST Send "))
        to_dump = "Request => " + str(http_headers) + "\n"
        analyze_response(args, response, to_dump)
    except Exception as e :
        print(visual.error("Request POST : " + str(e)))
        sys.exit()