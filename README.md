
# pip-license-gen

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

pip-license-gen はインストール済みパッケージのライセンスファイルをまとめて出力するコマンドを追加します。
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

## Install

```shell
pip install .
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2022-2026 tikubonn

[pip-license-gen](https://github.com/tikubonn/pip-license-gen) licensed under the [AGPLv3](./LICENSE).
