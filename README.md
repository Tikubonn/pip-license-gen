
# pip-license-gen

![](https://img.shields.io/badge/version-0.1.0-gray)
![](https://img.shields.io/badge/python-3.10-blue)
![](https://img.shields.io/github/license/tikubonn/pip-license-gen)

pip-license-gen はインストール済みパッケージのライセンスファイルを統合して出力するコマンドを追加します。
統合されたライセンスファイルを得るには `pip-license-gen` コマンドを実行します。

```cmd
pip-license-gen 
```

```txt
=========================================
License file 'LICENSE' of certifi.
https://github.com/certifi/python-certifi
=========================================

This package contains a modified version of ca-bundle.crt:

ca-bundle.crt -- Bundle of CA Root Certificates

Certificate data from Mozilla as of: Thu Nov  3 19:04:19 2011#
This is a bundle of X.509 certificates of public Certificate Authorities
(CA). These were automatically extracted from Mozilla's root certificates
file (certdata.txt).  This file can be found in the mozilla source tree:
http://mxr.mozilla.org/mozilla/source/security/nss/lib/ckfw/builtins/certdata.txt?raw=1#
It contains the certificates in PEM format and therefore
...
```

ライセンスを抽出するパッケージを指定することもできます（複数選択も可）。
パッケージが未指定ならばインストールされたすべてのパッケージが検索されます。

```cmd
pip-license-gen requests
```

```txt
===================================
License file 'LICENSE' of requests.
https://requests.readthedocs.io
===================================

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.
...
```

パッケージの中にはまれにライセンス情報が欠落しているものがあります。
pip-license-gen はJSON形式で記述された外部ファイルからライセンスファイルを作成することもできます。
これはパッケージ以外のライセンス情報を混ぜ込むときにも有用です。

```json
[
  {
    "Name": "json5",
    "Home-page": "https://github.com/json5/json5",
    "LicenseURLs": [
      "https://raw.githubusercontent.com/json5/json5/main/LICENSE.md"
    ]
  },
  {
    "Name": "ordered-set",
    "Home-page": "https://github.com/rspeer/ordered-set",
    "LicenseURLs": [
      "https://raw.githubusercontent.com/rspeer/ordered-set/master/MIT-LICENSE"
    ]
  },
  {
    "Name": "Python",
    "Home-page": "https://github.com/python/cpython",
    "LicenseURLs": [
      "https://raw.githubusercontent.com/python/cpython/9d38120e335357a3b294277fd5eff0a10e46e043/LICENSE"
    ]
  }
]
```

```cmd
pip-license-gen --from-json example.json
```

```txt
======================================================================================
License file 'https://raw.githubusercontent.com/json5/json5/main/LICENSE.md' of json5.
https://github.com/json5/json5
======================================================================================

MIT License

Copyright (c) 2012-2018 Aseem Kishore, and [others].

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

pip-license-gen は pip-tree と同様に pipenv にも対応しています。
`pipenv shell` もしくは `pipenv run` とともに使用することで pipenv 環境を参照するようになります。

```cmd
pipenv run pip-license-gen
```

```txt
======================================
License file 'LICENSE.txt' of aggdraw.
https://github.com/pytroll/aggdraw
======================================

The aggdraw interface, and associated modules and documentation are:

Copyright (c) 2011-2018 by AggDraw Developers
Copyright (c) 2003-2006 by Secret Labs AB
Copyright (c) 2003-2006 by Fredrik Lundh

By obtaining, using, and/or copying this software and/or its
associated documentation, you agree that you have read, understood,
and will comply with the following terms and conditions:

...
```

その他、細かい部分に関しては `pip-license-gen -h` コマンドをご参照ください。

```cmd
pip-license-gen -h
```

## Install

```cmd
python setup.py install
```

## Require packages 

* requests: https://github.com/psf/requests
* pip-tree: https://github.com/tikubonn/pip-tree 

## License 

The MIT License.
