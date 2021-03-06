# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def verify():
    """Verifies that a built Python distribution behaves as expected."""
    import sys

    sys.dont_write_bytecode = True

    import os

    here = os.path.dirname(sys.executable)
    install_root = os.path.dirname(here)

    # Need to set TCL_LIBRARY so local tcl/tk files get picked up.
    os.environ["TCL_LIBRARY"] = os.path.join(install_root, "lib", "tcl", "tcl")

    verify_compression()
    verify_ctypes()
    verify_curses()
    verify_hashlib()
    verify_sqlite()
    verify_ssl()
    verify_tkinter()

    print("distribution verified!")


def verify_compression():
    import bz2, lzma, zlib

    assert lzma.is_check_supported(lzma.CHECK_CRC64)
    assert lzma.is_check_supported(lzma.CHECK_SHA256)


def verify_ctypes():
    import ctypes

    assert ctypes.pythonapi is not None


def verify_curses():
    import curses

    curses.initscr()
    curses.endwin()


def verify_hashlib():
    import hashlib

    assert hashlib.algorithms_available == {
        "blake2b",
        "blake2b512",
        "blake2s",
        "blake2s256",
        "md4",
        "md5",
        "md5-sha1",
        "mdc2",
        "ripemd160",
        "sha1",
        "sha224",
        "sha256",
        "sha3-224",
        "sha3-256",
        "sha3-384",
        "sha3-512",
        "sha384",
        "sha3_224",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "sha512",
        "sha512-224",
        "sha512-256",
        "shake128",
        "shake256",
        "shake_128",
        "shake_256",
        "sm3",
        "whirlpool",
    }


def verify_sqlite():
    import sqlite3

    assert sqlite3.sqlite_version_info == (3, 29, 0)


def verify_ssl():
    import ssl

    assert ssl.HAS_TLSv1
    assert ssl.HAS_TLSv1_1
    assert ssl.HAS_TLSv1_2
    assert ssl.HAS_TLSv1_3

    assert ssl.OPENSSL_VERSION_INFO == (1, 1, 1, 3, 15)

    context = ssl.create_default_context()


def verify_tkinter():
    import tkinter as tk

    class Application(tk.Frame):
        def __init__(self, master=None):
            super().__init__(master)
            self.master = master
            self.pack()

            self.hi_there = tk.Button(self)
            self.hi_there["text"] = "Hello World\n(click me)"
            self.hi_there["command"] = self.say_hi
            self.hi_there.pack(side="top")

            self.quit = tk.Button(
                self, text="QUIT", fg="red", command=self.master.destroy
            )
            self.quit.pack(side="bottom")

        def say_hi(self):
            print("hi there, everyone!")

    root = tk.Tk()
    Application(master=root)


if __name__ == "__main__":
    verify()
