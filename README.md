# JWT-Intruder

JWT-Intruder is a Json Web Token construction, analysis and penetration tool coded in Python.
<span style="color: green"> Some green text </span>

## Installation
```bash
git clone https://github.com/Thomas97460/JWT-Intruder.git
```
## Usage
### Construction
```bash
python3 main.py -c -head '{"alg":"HS256"}' -play '{"user":"admin"}' -sk secret_key.txt
```
### Analyze
```bash
python3 main.py -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.JqU-Egztir5emS1kK8F8p8aOrJS8DLQWlyuDuINkjgc
```
### Bruteforce (Hashcat)
```bash
python3 main.py -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.QmddAIr_BZdQ7nUryc5KsZzq8TLod1YKTGFg_xte47o -f -w wordlist.txt
```
### None Algorithm
```bash

```

### Kid Injection
```bash

```

### Alg Injection
```bash

```

### Mismatch Algorithm
```bash

```

### Blank Password
```bash

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
