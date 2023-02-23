<div align="center">
  <img
    src="https://user-images.githubusercontent.com/24605263/214285260-80aed843-17e6-4a2f-98bf-bfb21f900dff.png"
    alt="kapak - A simple-to-use file encryption script"
  >
</div>

<div align="center">

[![tests](https://github.com/amis-shokoohi/kapak/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/amis-shokoohi/kapak/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/amis-shokoohi/kapak/branch/main/graph/badge.svg?token=6W2V3QOZKP)](https://codecov.io/gh/amis-shokoohi/kapak)
![GitHub](https://img.shields.io/github/license/amis-shokoohi/kapak)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/amis-shokoohi/kapak/main)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/amis-shokoohi/kapak)
![GitHub Repo stars](https://img.shields.io/github/stars/amis-shokoohi/kapak)
![GitHub forks](https://img.shields.io/github/forks/amis-shokoohi/kapak)

</div>

**Kapak** is a simple-to-use **file encryption** script/library.<br>
It uses `AES_256_CBC` as its encryption cipher.

> If you are wondering what _kapak_ means, it means _mold_.

- [Installation](#installation)
- [CLI Usage](#cli-usage)
  - [Encrypt file](#cli-usage-encrypt-file)
  - [Encrypt stdin](#cli-usage-encrypt-stdin)
  - [Password file](#cli-usage-password-file)
- [Integration](#integration)
  - [Encrypt file](#integration-encrypt-file)
  - [Encrypt stdin](#integration-encrypt-stdin)
  - [Encrypt anything](#integration-encrypt-anything)

<span id="installation"></span>

## Installation

Installing with `pip`:

```
pip install kapak
```

<span id="cli-usage"></span>

## CLI Usage

```
kapak [global options] [command] [command options] [input]
kapak [encrypt | e] [options] [input]
kapak [decrypt | d] [options] [input]
```

<span id="cli-usage-encrypt-file"></span>

### Encrypt file

```
$ kapak encrypt -o ./image.jpg.kpk ./image.jpg
Enter password:
Confirm password:
■■■■■■■■■■ 100%
```

```
$ kapak decrypt -o ./image.jpg ./image.jpg.kpk
Enter password:
■■■■■■■■■■ 100%
```

<span id="cli-usage-encrypt-stdin"></span>

### Encrypt stdin

```
$ echo 'secret stuff' | kapak encrypt | base64
Enter password:
Confirm password:
AAAAbWth...t/ILJW/v
```

```
$ echo 'AAAAbWth...t/ILJW/v' | base64 --decode | kapak decrypt
Enter password:
secret stuff
```

```
$ cat ./text.txt | kapak encrypt -b 1024 > ./text.txt.kpk
Enter password:
Confirm password:
```

```
$ kapak decrypt -b 1024 ./text.txt.kpk > ./text.txt
Enter password:
```

<span id="cli-usage-password-file"></span>

### Password file

```
$ echo 'P@ssw0rd' > ./password.txt
$ kapak encrypt -p ./password.txt -o ./image.jpg.kpk ./image.jpg
■■■■■■■■■■ 100%
```

```
$ kapak decrypt -p ./password.txt -o ./image.jpg ./image.jpg.kpk
■■■■■■■■■■ 100%
```

<span id="integration"></span>

## Integration

<span id="integration-encrypt-file"></span>

### Encrypt file

```py
from pathlib import Path
from kapak.aes import encrypt

input_file = Path("image.jpg")
output_file = Path("image.jpg.kpk")

with input_file.open("rb") as src, output_file.open("wb") as dst:
    total_len = input_file.stat().st_size
    progress = 0
    for chunk_len in encrypt(src, dst, "P@ssw0rd"):
        progress += chunk_len
        print(f"{progress}/{total_len}")
```

> `kapak.aes.encrypt` is a generator. It yields the length of encrypted data on every iteration.

```py
from pathlib import Path
from itertools import accumulate
from kapak.aes import decrypt

input_file = Path("image.jpg.kpk")
output_file = Path("image.jpg")

with input_file.open("rb") as src, output_file.open("wb") as dst:
    total_len = input_file.stat().st_size
    for progress in accumulate(decrypt(src, dst, "P@ssw0rd")):
        print(f"{progress}/{total_len}")
```

> `kapak.aes.decrypt` is a generator. It yields the length of decrypted data on every iteration.

<span id="integration-encrypt-stdin"></span>

### Encrypt stdin

```py
import sys
from io import BytesIO
from kapak.aes import encrypt

with BytesIO() as dst:
    for _ in encrypt(
        src=sys.stdin.buffer,
        dst=dst,
        password="P@ssw0rd",
        buffer_size=1024
    ):
        pass
    encrypted_data = dst.getvalue()
    print(encrypted_data.hex())
```

<span id="integration-encrypt-anything"></span>

### Encrypt anything

```py
from io import BytesIO
from kapak.aes import encrypt

anything = b"anything"

with BytesIO(anything) as src, BytesIO() as dst:
    for _ in encrypt(
        src=src,
        dst=dst,
        password="P@ssw0rd",
        buffer_size=1024
    ):
        pass
    encrypted_data = dst.getvalue()
    print(encrypted_data.hex())
```
