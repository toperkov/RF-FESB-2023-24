# RF - Lab 1: BitLocker i dekripcija diska

Kako bi zaštitili laptope, vanjske diskove, USB memorije od posljedica krađe, veoma često se upotrebljavaju tehnike enkripcije cijelih memorija. Jedna od tehnika zaštite podataka je korištenje **BitLocker** alata za šifriranje diska koje je dostupan u novijim verzijama Windowsa (Vista, 7, 8.1 i 10) Ultimate, Pro i Enterprise.

**ZADATAK:** Pretpostavite da ste dobili na analizu USB memoriju čiji je sadržaj enkriptiran korištenjem BitLockera. Nakon što ste napravili sigurnosnu kopiju USB memorije, vaš zadatak je saznati lozinku kojom je enkriptiran disk/USB.

## Postupak probijanja Bitlocker lozinke

Probijanje lozinke se sastoji od dva dijela: izvlačenje hash sadržaja iz sigurnosne kopije UBS-a koji je zaštićen lozinkom te stvarnog napada. Sačuvajte na računalu sliku USB-a koji se nalazi na [OneDrive-u](https://fesb-my.sharepoint.com/:u:/g/personal/toperkov_fesb_hr/ERP3tpm9FRRIkk82lCHbQpIBGu-9efbxohQv6dZ6g2B2AQ?e=vmHmwi).

```python
import requests
def download_file_with_custom_headers(url, local_filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()  # This will throw an exception for non-200 responses
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    print("File downloaded successfully.")


# Example usage
file_url = 'https://fesb-my.sharepoint.com/:u:/g/personal/toperkov_fesb_hr/ERP3tpm9FRRIkk82lCHbQpIBGu-9efbxohQv6dZ6g2B2AQ?download=1'
output_dir = './imageFESB.001'
download_file_with_custom_headers(file_url, output_dir)
```

### Izračun Hash vrijednosti kopije USB-a

Vaš zadatak je provjeriti odgovara li SHA1 hash vrijednost kopije USB-a onoj koju Vam je dao profesor.

```python
import hashlib

def verify_image_hash(image_path, given_hash):
    """
    Verifies the integrity of an image file by comparing its SHA-1 hash against a given hash.

    Parameters:
    - image_path (str): The file path to the image whose integrity is being verified.
    - given_hash (str): The expected SHA-1 hash value for the image file.

    Returns:
    - bool: True if the image's SHA-1 hash matches the given hash, False otherwise.
    """
    try:
        # Compute the SHA-1 hash of the image file
        with open(image_path, 'rb') as f:
            computed_hash = hashlib.sha1(f.read()).hexdigest()

        # Compare the computed hash with the given hash
        if computed_hash == given_hash:
            print('Bitstream image verified successfully.')
            return True
        else:
            print('Error: Bitstream image verification failed.')
            return False
    except IOError as e:
        print(f"Error opening file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# Example usage
image_path = 'imageFESB.001'
given_hash = "201cdee056cfc8c0996328e3c2115b513a141f5c"
verify_image_hash(image_path, given_hash)
```



### Izvlačenje hash vrijednosti - [John the Ripper](https://www.openwall.com/john/)

Na računalu sačuvajte sigurnosnu kopiju USB-a koji je enkriptiran BitLockerom. Nakon toga, skinite verziju alata John the Ripper na ovom [LINK-u](https://fesb-my.sharepoint.com/:u:/g/personal/toperkov_fesb_hr/EYTWFYb1RkBDkUrBcTfucmcB9TJEFSjTEeiwfVcsCIV63g?download=1) te ga raspakirajte. To možete postići tako da kombinirate kod iz prvog dijela zadatka sa ovim dolje. Prije korištenja instalirajte biblioteku `pyunpack`:

```python
pip install pyunpack
```

```python
from pyunpack import Archive
import os

def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory '{directory_path}' created or already exists.")
    except Exception as e:
        print(f"Failed to create directory '{directory_path}': {e}")

# Example usage
directory_path = 'john-1.9.0-jumbo-1-win64'
create_directory(directory_path)

Archive('john-1.9.0-jumbo-1-win64.zip').extractall("john-1.9.0-jumbo-1-win64")
```

U nastavku izvucite hash korištenjem `bitlocker2john` alata. Trebali bi dobiti nešto slično u nastavku:

```python
Signature found at 0x00010003
Version: 8
Invalid version, looking for a signature with valid version...

Signature found at 0x02110000
Version: 2 (Windows 7 or later)

VMK entry found at 0x021100d2
VMK encrypted with user password found!
VMK encrypted with AES-CCM

VMK entry found at 0x021101b2
VMK encrypted with Recovery key found!
VMK encrypted with AES-CCM

$bitlocker$0$16$a149a1c91be871e9783f51b59fd9db88$1048576$12$b0adb333606cd30103000000$60$c1633c8f7eb721ff42e3c29c3daea6da0189198af15161975f8d00b8933681d93edc7e63f36b917cdb73285f889b9bb37462a40c1f8c7857eddf2f0e
$bitlocker$1$16$a149a1c91be871e9783f51b59fd9db88$1048576$12$b0adb333606cd30103000000$60$c1633c8f7eb721ff42e3c29c3daea6da0189198af15161975f8d00b8933681d93edc7e63f36b917cdb73285f889b9bb37462a40c1f8c7857eddf2f0e
$bitlocker$2$16$2f8c9fbd1ed2c1f4f034824f418f270b$1048576$12$b0adb333606cd30106000000$60$8323c561e4ef83609aa9aa409ec5af460d784ce3f836e06cec26eed1413667c94a2f6d4f93d860575498aa7ccdc43a964f47077239998feb0303105d
$bitlocker$3$16$2f8c9fbd1ed2c1f4f034824f418f270b$1048576$12$b0adb333606cd30106000000$60$8323c561e4ef83609aa9aa409ec5af460d784ce3f836e06cec26eed1413667c94a2f6d4f93d860575498aa7ccdc43a964f47077239998feb0303105d
```

Kao što je prikazano u primjeru, `bitlocker2john` vraća 4 izlazna hasha s različitim prefiksom.

- Ako je uređaj šifriran metodom provjere autentičnosti korisničke lozinke, `bitlocker2john` ispisuje ta dva hasha:
  - `$bitlocker$0$...:` pokreće način brzog napada korisničke lozinke
  - `$bitlocker$1$...:` pokreće način napada korisničke lozinke s MAC provjerom (sporije izvršavanje, bez _false positives_ rezultata)

- U svakom slučaju, `bitlocker2john` ispisuje sljedeća dva hasha:
  - `$bitlocker$2$...:` pokreće način brzog napada lozinke za oporavak
  - `$bitlocker$3$...:` pokreće način napada za oporavak lozinke s MAC provjerom (sporije izvršavanje, bez _false positives_ rezultata)

Opći format za liniju izlaza `bitlocker2john` je:
```python
$bitlocker$version$salt_length$salt$iterations$vmk_length$vmk$mac_length$mac
```
U nastavku je dano objašnjenje za svaki segment detaljnije:
-   **`$bitlocker$`** - Identifikator za format BitLocker hash-a.
-   **`0`** - Verzija metode enkripcije.
-   **`16`** - Dužina soli (u bajtovima).
-   **`a149a1c91be871e9783f51b59fd9db88`** - Vrijednost soli.
-   **`1048576`** - Broj iteracija za funkciju derivacije ključa.
-   **`12`** - Dužina šifriranog VMK (Volume Master Key) (u bajtovima).
-   **`b0adb333606cd30103000000`** - Šifrirani VMK.
-   **`60`** - Dužina MAC-a.
-   **`c163...2f0e`** - Stvarni podaci za provjeru je li pogađana lozinka točna.

S obzirom na ovu strukturu, proces pogađanja ključa (ili preciznije, lozinke ili PIN-a koji dešifriraju VMK) uključuje korištenje svakog elementa ovog podatka u alatu za probijanje lozinki za testiranje svake kandidat-lozinke. Postupak izvlačenja se može automatizirati kroz python kod te se rezultat pohranjuje u varijablu ``recovery_key`` umjesto u datoteku:

```python
import socket
import subprocess

# Set the path to the USB image file
image_path = 'imageFESB.001'

# Call bitlocker2john to extract the recovery key
bitlocker2john_cmd = f'bitlocker2john -i {image_path}'
process = subprocess.Popen(bitlocker2john_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, error = process.communicate()

# Print the extracted recovery key
keys = output.decode().strip().split('\n')
recovery_key = [s for s in keys if "$bitlocker$1$" in s]
print(f'BitLocker recovery key: {recovery_key[0]}')
```

### Probijanje lozinke - [Hashcat](https://hashcat.net/hashcat/)

U nastavku ćemo upotrebljavati alat Hashcat kako bismo automatizirali postupak probijanja ključa enkriptiranog diska. U terminalu instalirajte hashcat sa naredbom:
```python
pip install hashcat
```
U nastavku ćemo koristiti naredbu za probijanje BitLocker lozinke korištenjem `Hashcat`:
```python
hashcat -m 22100 -a 3 {recovery_key[0]} "xyz?d?d?d?d?d"
```

pri čemu `-m 22100` predstavlja hash mode za BitLocker, `xyz` predstavlja **HINT** kojeg ćete dobiti od profesora, a `?d?d?d?d?d` je niz od 5 brojeva koji hashcat mora pogoditi _bruteforce_ napadom.


Nakon toga ažurirajte python skriptu da biste realizirali napad:

```python
output_file = hash.txt
hashcat_cmd = f'hashcat -m 22100 -a 3 {recovery_key[0]} --potfile-disable --remove --outfile {output_file} "xyzk?d?d?d?d"'
process = subprocess.call(hashcat_cmd, shell=True)

# Execute hashcat command using subprocess
try:
    output = subprocess.check_output(hashcat_cmd, shell=True)
    print(output.decode("utf-8"))
except subprocess.CalledProcessError as e:
    print(f"Error executing hashcat command: {e}")
```

U pozadini, Hashcat radi pogađa ključ prema sljedećem pseudokodu:
```python
function crack_bitlocker_hash(hash_line):
    parts = split(hash_line, '$')
    salt = parts[3]
    iterations = int(parts[4])
    encrypted_vmk = parts[6]
    mac_length = int(parts[7])
    mac_data = parts[8]
    
    for each password_candidate in password_list:
        derived_key = derive_key(password_candidate, salt, iterations)
        decrypted_vmk = decrypt(encrypted_vmk, derived_key)
        
        if verify_mac(decrypted_vmk, mac_data, mac_length):
            print("Password found:", password_candidate)
            return password_candidate
    
    print("Password not found.")
    return None

function derive_key(password, salt, iterations):
    # Pseudocode for deriving a key from a password, using a KDF with specified iterations
    # This would mimic the BitLocker KDF process
    return derived_key

function decrypt(data, key):
    # Pseudocode for decrypting data with a key
    # This would mimic the BitLocker decryption process for the VMK
    return decrypted_data

function verify_mac(decrypted_vmk, mac_data, mac_length):
    # Pseudocode for verifying if the decrypted VMK matches the expected MAC
    # This is how you confirm if the guessed password is correct
    return True or False

# Example usage
hash_line = "$bitlocker$0$16$a149a1c91be871e9783f51b59fd9db88$1048576$12$b0adb333606cd30103000000$60$c1633c8f7eb721ff42e3c29c3daea6da0189198af15161975f8d00b8933681d93edc7e63f36b917cdb73285f889b9bb37462a40c1f8c7857eddf2f0e"
crack_bitlocker_hash(hash_line)
```

## Napredni napad

> **EDIT:**  
> Korištenjem Cloud infrastrukture pokušajte ponoviti probijanje lozinke upotrebom [Hashtopollis](https://nikita-guliaev.medium.com/clustering-hashcat-with-hashtopolis-for-distributed-cloud-computing-55f964a56804) alata te usporedite vrijeme potrebno za doznavanje lozinke u odnosnu sa vrijeme na računalu.

## Podizanje slike kopije diska korištenjem Arsenal Image Mounter alata

Na računalo sačuvajte [Arsenal Image Mounter](https://fesb-my.sharepoint.com/:u:/g/personal/toperkov_fesb_hr/ERwLM1Ar3YhKv9PN80yMGRABXX_phmOooJpKEsQOwPIdow?download=1) s kojom ćemo podigniti sigurnosnu kopiju USB-a u _Read-only modu_. Kada stisnete tipku `Mount Image`, pronađite sigurnosnu kopiju diska, označite `Read only` te `Create "removable" disk device`. Nakon toga bi se trebao pokazati BitLocker prozor upozorenja za unos lozinke. Kada unesete lozinku trebao bi se pojaviti sadržaj USB memorije.