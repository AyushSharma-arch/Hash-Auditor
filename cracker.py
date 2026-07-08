#!/usr/bin/env python3

import argparse
import hashlib
import hmac
import math
import re
from pathlib import Path


SUPPORTED_ALGOS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def get_hasher(algo: str):
    algo = algo.lower().strip()

    if algo not in SUPPORTED_ALGOS:
        raise ValueError(f"Unsupported algorithm: {algo}")

    return SUPPORTED_ALGOS[algo]()


def hash_text(text: str, algo: str) -> str:
    hasher = get_hasher(algo)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def hash_file(file_path: str, algo: str, chunk_size: int = 8192) -> str:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    hasher = get_hasher(algo)

    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()


def verify_text_hash(text: str, expected_hash: str, algo: str) -> bool:

    calculated = hash_text(text, algo)

    return hmac.compare_digest(
        calculated.lower(),
        expected_hash.lower().strip()
    )


def verify_file_hash(file_path: str, expected_hash: str, algo: str) -> bool:

    calculated = hash_file(file_path, algo)

    return hmac.compare_digest(
        calculated.lower(),
        expected_hash.lower().strip()
    )


def password_strength(password: str):

    length = len(password)

    score = 0

    if length >= 8:
        score += 1

    if length >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(not c.isalnum() for c in password):
        charset += 33

    entropy = 0

    if charset:
        entropy = round(length * math.log2(charset), 2)

    if score <= 2:
        rating = "Weak"

    elif score <= 4:
        rating = "Moderate"

    else:
        rating = "Strong"

    return {
        "length": length,
        "rating": rating,
        "score": score,
        "entropy": entropy,
    }


def print_strength_report(password: str):

    report = password_strength(password)

    print("\n========== PASSWORD ANALYSIS ==========")
    print(f"Length      : {report['length']}")
    print(f"Rating      : {report['rating']}")
    print(f"Score       : {report['score']}/6")
    print(f"Entropy     : {report['entropy']} bits")
    print("=======================================")


def menu():

    print("\n========== HASH AUDITOR ==========")
    print("1. Generate Text Hash")
    print("2. Generate File Hash")
    print("3. Verify Text Hash")
    print("4. Verify File Hash")
    print("5. Password Strength")
    print("6. Exit")
def main():

    parser = argparse.ArgumentParser(
        description="Hash Auditor for integrity, verification, and password-strength analysis"
    )

    parser.add_argument(
        "--algo",
        default="sha256",
        choices=list(SUPPORTED_ALGOS.keys()),
        help="Hash algorithm"
    )

    parser.add_argument(
        "--text",
        help="Text input"
    )

    parser.add_argument(
        "--file",
        help="File path"
    )

    parser.add_argument(
        "--verify",
        help="Expected hash"
    )

    parser.add_argument(
        "--strength",
        help="Check password strength"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactive mode"
    )

    parser.add_argument(
        "--identify",
        help="Identify hash type"
    )

    args = parser.parse_args()

    # -----------------------------
    # HASH IDENTIFIER
    # -----------------------------
    if args.identify:

        hash_input = args.identify.strip()

        print("\n========== HASH ANALYSIS ==========")
        print(f"Hash Value : {hash_input}")

        if len(hash_input) == 32:
            print("Algorithm  : MD5")
            print("Length     : 32 Characters")
            print("Risk Level : Weak")

        elif len(hash_input) == 40:
            print("Algorithm  : SHA1")
            print("Length     : 40 Characters")
            print("Risk Level : Weak")

        elif len(hash_input) == 56:
            print("Algorithm  : SHA224")
            print("Length     : 56 Characters")
            print("Risk Level : Moderate")

        elif len(hash_input) == 64:
            print("Algorithm  : SHA256")
            print("Length     : 64 Characters")
            print("Risk Level : Strong")

        elif len(hash_input) == 96:
            print("Algorithm  : SHA384")
            print("Length     : 96 Characters")
            print("Risk Level : Very Strong")

        elif len(hash_input) == 128:
            print("Algorithm  : SHA512")
            print("Length     : 128 Characters")
            print("Risk Level : Very Strong")

        else:
            print("Algorithm  : Unknown")

        print("===================================")

        return

    # -----------------------------
    # INTERACTIVE MODE
    # -----------------------------
    if args.interactive:

        while True:

            menu()

            choice = input("Select option: ").strip()

            try:

                if choice == "1":

                    text = input("Enter Text : ")

                    algo = input(
                        "Algorithm (md5/sha1/sha256/sha512): "
                    ).strip().lower()

                    print("\nHash:")
                    print(hash_text(text, algo))
                elif choice == "2":

                    file_path = input("Enter File Path : ")

                    algo = input(
                        "Algorithm (md5/sha1/sha256/sha512): "
                    ).strip().lower()

                    print("\n========== FILE HASH ==========")
                    print(hash_file(file_path, algo))
                    print("================================")

                elif choice == "3":

                    text = input("Enter Text : ")

                    expected = input(
                        "Enter Expected Hash : "
                    )

                    algo = input(
                        "Algorithm (md5/sha1/sha256/sha512): "
                    ).strip().lower()

                    result = verify_text_hash(
                        text,
                        expected,
                        algo
                    )

                    if result:

                        print("\n========== HASH VERIFICATION ==========")
                        print("Status      : VERIFIED")
                        print("Result      : MATCH FOUND")
                        print("Integrity   : PASSED")
                        print("=======================================")

                    else:

                        print("\n========== HASH VERIFICATION ==========")
                        print("Status      : FAILED")
                        print("Result      : NO MATCH")
                        print("Integrity   : FAILED")
                        print("=======================================")
                elif choice == "4":

                    file_path = input("Enter File Path : ")

                    expected = input(
                        "Enter Expected Hash : "
                    )

                    algo = input(
                        "Algorithm (md5/sha1/sha256/sha512): "
                    ).strip().lower()

                    result = verify_file_hash(
                        file_path,
                        expected,
                        algo
                    )

                    if result:

                        print("\n========== FILE VERIFICATION ==========")
                        print("Status      : VERIFIED")
                        print("Result      : MATCH FOUND")
                        print("Integrity   : PASSED")
                        print("=======================================")

                    else:

                        print("\n========== FILE VERIFICATION ==========")
                        print("Status      : FAILED")
                        print("Result      : NO MATCH")
                        print("Integrity   : FAILED")
                        print("=======================================")

                elif choice == "5":

                    password = input(
                        "Enter Password : "
                    )

                    print_strength_report(password)

                elif choice == "6":

                    print("\nExiting Hash Auditor...")
                    break

                else:

                    print("\nInvalid Choice.")

            except Exception as e:

                print(f"\nError : {e}")

        return

    # ----------------------------------
    # PASSWORD STRENGTH (CLI MODE)
    # ----------------------------------
    if args.strength:
        print_strength_report(args.strength)
        return

    # ----------------------------------
    # VERIFY TEXT HASH
    # ----------------------------------
    if args.text and args.verify:

        ok = verify_text_hash(
            args.text,
            args.verify,
            args.algo
        )

        if ok:
            print("\n========== HASH VERIFICATION ==========")
            print("Status      : VERIFIED")
            print("Result      : MATCH FOUND")
            print("Integrity   : PASSED")
            print("=======================================")
        else:
            print("\n========== HASH VERIFICATION ==========")
            print("Status      : FAILED")
            print("Result      : NO MATCH")
            print("Integrity   : FAILED")
            print("=======================================")

        return

    # ----------------------------------
    # VERIFY FILE HASH
    # ----------------------------------
    if args.file and args.verify:

        ok = verify_file_hash(
            args.file,
            args.verify,
            args.algo
        )

        if ok:
            print("\n========== FILE VERIFICATION ==========")
            print("Status      : VERIFIED")
            print("Result      : MATCH FOUND")
            print("Integrity   : PASSED")
            print("=======================================")
        else:
            print("\n========== FILE VERIFICATION ==========")
            print("Status      : FAILED")
            print("Result      : NO MATCH")
            print("Integrity   : FAILED")
            print("=======================================")

        return

    # ----------------------------------
    # GENERATE TEXT HASH
    # ----------------------------------
    if args.text:

        hash_value = hash_text(
            args.text,
            args.algo
        )

        print("\n========== HASH GENERATED ==========")
        print(f"Input Text : {args.text}")
        print(f"Algorithm  : {args.algo.upper()}")
        print(f"Hash       : {hash_value}")
        print("====================================")

        return

    # ----------------------------------
    # GENERATE FILE HASH
    # ----------------------------------
    if args.file:

        file_hash_value = hash_file(
            args.file,
            args.algo
        )

        print("\n========== FILE HASH REPORT ==========")
        print(f"File      : {args.file}")
        print(f"Algorithm : {args.algo.upper()}")
        print(f"Hash      : {file_hash_value}")
        print("======================================")

        return

    parser.print_help()


if __name__ == "__main__":
    main()