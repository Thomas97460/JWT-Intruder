# JWT-Intruder

JWT-Intruder is a Json Web Token construction, analysis and penetration tool coded in Python.
For now, only HS256/512 and RS256/512 algorithms are supported.

## Installation
```bash
git clone https://github.com/Thomas97460/JWT-Intruder.git
```
## Usage
### Usage with -u URL parameter
#### Classic
You can add ```-u https://yourtarget.com``` in order to send the token to your target. The request will be sent in ```-get ``` by default or you can specify the paramter ```-post```. The token is placed in the ```HTTP Authorization : Bearer YOURTOKEN``` header field and in cookies ```jwt : YOURTOKEN```.

#### Search parameter
The ```-find``` parameter is used to locate character strings in the server's response. The parameter expects a list in json format : ```-find '["flag","password","admin"]'```.

#### https headers optional fields


- ### Construction
```bash
python3 main.py -c -head '{"alg":"HS256"}' -play '{"user":"admin"}' -sk secret_key.txt
```
- ### Analyze
```bash
python3 main.py -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.JqU-Egztir5emS1kK8F8p8aOrJS8DLQWlyuDuINkjgc
```
- ### Bruteforce (Hashcat)
```bash
python3 main.py -f -w wordlist.txt \
-t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o 
```
- ### None Algorithm
#### Local
```bash
python3 main.py -n -t \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o
```
#### Attack with url
```bash
python3 main.py -n -t -find '["google"]' -u https://google.com \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o
```
- ### Kid Injection
#### Local
```bash
python3 main.py -k -w inject.txt -out output.txt -sk sec_key.txt -t \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o
```
#### Attack with url
```bash
python3 main.py -k -w inject.txt -u https://google.com -sk sec_key.txt -t \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o
```

- ### Alg Injection
#### Local
```bash
python3 main.py -alg -out out.txt -w inject.txt -t \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o
```
#### Attack with url
```bash
python3 main.py -alg -w inject.txt -u https://google.com -t\
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o
```
- ### Mismatch Algorithm
#### Local
```bash
python3 main.py -ms -p pub_key.txt -t \
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.F7TSgnhXiCKuaveFaQMjJv4nkeW8sDU-7m-3zhAVanxYN8ZR0raPYcSqr1tb3i84_7vd7ZY2rFDhjgRELATjSzJPzf6Rf5Q_g0ljMZpIL1xrFdhqkVwC8-VcIB3M-oovS_8Ys1w75H2K9v9KPHoL0z_nvEhkrv8MG17_mSzz9eA
```
#### Attack with url
```bash
python3 main.py -ms -p pub_key.txt -u https://google.com -t \
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.F7TSgnhXiCKuaveFaQMjJv4nkeW8sDU-7m-3zhAVanxYN8ZR0raPYcSqr1tb3i84_7vd7ZY2rFDhjgRELATjSzJPzf6Rf5Q_g0ljMZpIL1xrFdhqkVwC8-VcIB3M-oovS_8Ys1w75H2K9v9KPHoL0z_nvEhkrv8MG17_mSzz9eA
```

- ### Blank Password
#### Local
```bash
python3 main.py -b -t \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.Mj1JXmT8qYRC1hNw-1BPEZELQSwYNefFCYPTYzZcqLU
```
#### Attack with url 
```bash
python3 main.py -b -u https://google.com -t \
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.Mj1JXmT8qYRC1hNw-1BPEZELQSwYNefFCYPTYzZcqLU
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
