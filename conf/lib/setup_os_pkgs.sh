#!/bin/bash

setup_os_packages() {

    PACKAGES_FILE="$1"

    echo ">>> OSTYPE =$OSTYPE, $PACKAGES_FILE"

    [[ "$OSTYPE" == "linux-gnu"* ]] && {
        echo "「インフォ」Linux type detected, assuming Debian..."
        cat "$PACKAGES_FILE" | xargs apt-get install -y
        return 0
    }
    [[ "$OSTYPE" == "darwin"* ]] && {
        echo "「インフォ」MacOS type detected, assuming Brew..."
        cat "$PACKAGES_FILE" | xargs brew install
        return 0
    }

    [[ "$OSTYPE" == "cygwin" ]] && {
        echo "「インフォ」CYGWIN type detected, UNSUPORTED"
        # POSIX compatibility layer and Linux environment emulation for Windows
        return -1
    }
    [[ "$OSTYPE" == "msys" ]] && {
        echo "「インフォ」MS, assuming Debian..., UNSUPPORTED"
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
        return -1
    }
    [[ "$OSTYPE" == "win32" ]] && {
        echo "「インフォ」WIN32 type detected, UNSUPPORTED"
        # I'm not sure this can happen.
        return -1
    }
    [[ "$OSTYPE" == "freebsd"* ]] && {
        echo "「インフォ」FreeBSD type detected, UNSUPPORTED"
        return -1
    }

}