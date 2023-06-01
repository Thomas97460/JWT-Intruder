import argparse

def get_attack_args(args) :
    attack_args = [args.none_alg, args.kid, args.blank, args.mismatch, args.alg_injection]
    return attack_args

def count_nb_args_attack(group_attack):
    count = 0
    attack_args = get_attack_args(group_attack)
    for mode in attack_args :
        if mode:
            count += 1
    return count

def get_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', dest='token', required=False, help='JWT token')
    parser.add_argument('-u', '--url', dest='url', required=False, help='url')
    parser.add_argument('-p', '--pub_key', dest='public_key', required=False, help='filename of public key for RSA verification')
    parser.add_argument('-sk', '--sec_key', dest='secret_key', required=False, help='filename of secret key for RSA/HMAC encoding/verification')
    parser.add_argument('-w', '--wordlist', dest='wordlist', help='wordlist for bruteforce attack HMAC or Injection')
    parser.add_argument('-f', '--force', dest='bruteforce', action='store_true', help='bruteforce exploit')
    parser.add_argument('-c', '--construct', dest='construct', action='store_true', help='construction of token with HMAC')
    parser.add_argument('-head', '--head', dest='head', help='the content of the headers of the token in construction (all without typ)')
    parser.add_argument('-play', '--play', dest='play', help='the playload of the token in construction')
    parser.add_argument('-headers', '--headers', dest='headers', help='optional headers for http request in a txt file on json format')
    parser.add_argument('-cookies', '--cookies', dest='cookies', help='optional cookies')
    parser.add_argument('-get', '--get', dest='get', action='store_true', help='send get request (automatical)')
    parser.add_argument('-post', '--post', dest='post', action='store_true', help='send post request')
    parser.add_argument('-data', '--data', dest='data', help='send data in post request')
    parser.add_argument('-playload', '--playload', dest='playload', help='add this data in playload (json)')
    parser.add_argument('-new_playload', '--new_playload', dest='new_playload', help='replace this data in playload (json)')
    parser.add_argument('-find', '--find', dest='find', help='string to locate on the response')
    parser.add_argument('-output', '--output', dest='output', help='file to dump request response or result')
    parser.add_argument('-ms', '--mismatch', dest='mismatch', action='store_true', help='missmatch HS->RS exploit') 
    parser.add_argument('-alg', '--alg', dest='alg_injection', action='store_true', help='change the alg value withtout re sign the token')
    group_attack = parser.add_argument_group('attack options')
    group_attack.add_argument('-n', '--none', dest='none_alg', action='store_true', help='none algorithm exploit')
    group_attack.add_argument('-k', '--kid', dest='kid', action='store_true', help='kid injection exploit')
    group_attack.add_argument('-b', '--blank', dest='blank', action='store_true', help='blank password exploit (json list)')
    args = parser.parse_args()
    if args.token is None and not args.construct :
        parser.error("You need to provide a token with -t TOKEN or construct one with -c")
    if args.bruteforce and args.url is not None :
        parser.error("Une attaque par brute force se fait localement sans -u URL")
    elif args.bruteforce and args.wordlist is None :
        parser.error("Une attaque par brute force -f nécessite un fichier -w wordlist.txt")
    elif args.url is not None and count_nb_args_attack(args) != 1 :
        parser.error('Si -u ou --url est défini, un seul argument du groupe attack doit être défini.')
    # elif args.url is None and count_nb_args_attack(args) > 0 and not args.mismatch and not args.kid and not args.alg_injection :
    #     parser.error('Si -u ou --url n\'est défini, vous ne pouvez pas spécifiez d\'attaque.')
    elif args.url is None and (args.cookies is not None or args.headers is not None) :
        parser.error("Les cookies et headers sont applicables seulement avec un paramètre -u URL valide")
    elif args.url is None and (args.get or args.post) :
        parser.error("Les paramètres get et post sont applicables seulement avec un paramètre -u URL valide")
    elif args.url is not None and args.post is False and args.data is not None :
        parser.error("Le champ data est applicable seulement avec le paramètre -post et -u URL")
    elif args.url is None and (args.playload is not None or args.new_playload is not None) and not args.mismatch :
        parser.error("L'ajout de playload peut être utilisé seulement avec -u URL et une attaque (peut fausser la signature si l'exploit n'aboutit pas)")
    elif args.playload and args.new_playload :
        parser.error("Les arguments -playload et -new_playload ne peuvent pas être utilisé ensemble")
    elif args.url is None and args.find is not None :
        parser.error("find argument need -u URL parameters")
    elif args.url is None and args.output is not None and args.kid is None :
        parser.error("-output need a paramter -u URL to be used")
    # elif (args.url is not None or args.token is not None) and (args.construct or args.head is not None or args.play is not None) and args.kid is False:
    #     parser.error("construction of token is impossible with -u URL paramter or -t Token parameter")
    elif args.construct and (args.head is None or args.play is None) :
        parser.error("construction need parameter -head json_HEADER and -play json_PLAYLOAD")
    elif args.construct and args.secret_key is None :
        parser.error("-construct need -sk SECRET_KEY.txt/pem to sign the token in construction")
    elif args.mismatch and (args.public_key is None or args.token is None) :
        parser.error("Mismatch exploit need public RSA Key with -p FILENAME")
    elif args.kid and args.wordlist is None :
        parser.error("Kid Injection need a wordlist -w WORDLIST.TXT ")
    elif args.kid and args.url is None and args.output is None :
        parser.error("Kid Injection need a -u URL OR a -out OUTPUT.TXT")
    elif args.kid and not args.secret_key :
        parser.error("Kid Injection need -sk SECRET_KEY to sign tokens")
    elif args.alg_injection and args.output is None and args.url is None :
        parser.error("Alg injection need at least a -output OUTPUT parameter or a -u URL parameter")
    elif args.alg_injection is True and args.wordlist is None :
        parser.error("Alg injection need a -wordlist WORDLIST.txt parameter to perform the injection")
    elif args.blank is True and args.url is None and args.output is not None :
        parser.error("Blank attack can't take an -out output.txt argument without a url parameter")
    return args


