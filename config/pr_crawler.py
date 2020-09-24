# pylint: skip-file
"""
Download all files from opened pull request
"""

import os
import sys
import urllib3
import argparse
from cryptography.fernet import Fernet

from requests import get


def load_key() -> bytes:
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open('config/secret.key', 'rb').read()


def decrypt_message(encrypted_message: bytes) -> str:
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()


def get_by_url(url: str):
    encrypted = b'gAAAAABfbE7eXkXz9DNtehmlk3jSOtoss_8vvkxHNZm9BzdZ16sSI9su9k4Wka_frv5v54oHafz5Y0FaGR7HianCZd7Us6uxcDA9WWgCMvTQM-4QsOMKXQ6ZRXodFJ70MIq3WTB0KtWf'
    token = decrypt_message(encrypted)

    headers = {'Authorization': f'token {token}'}
    response = get(url, headers=headers)
    content = response.json()
    return content


def download_file(from_url: str, to_url: str) -> None:
    http = urllib3.PoolManager()
    req = http.request('GET', from_url, preload_content=False)

    with open(to_url, 'wb') as out:
        while True:
            data = req.read(100)
            if not data:
                break
            out.write(data)
    req.release_conn()


def main(lab_n: int, current_pr_id: int):
    if 'TRAVIS_COMMIT' not in os.environ:
        print('Need proper environment variables')
        sys.exit(1)

    current_commit_hash = os.environ.get('TRAVIS_COMMIT', 'None')

    base_url = 'https://api.github.com/repos/fipl-hse/2020-2-level-labs'

    content = get_by_url(url='{}/pulls?state=all'.format(base_url))
    for pull_req in content:
        pr_id = pull_req['number']
        if current_pr_id == pr_id:  # Skip PR so that main.py from current PR is not downloaded
            continue
        files_from_pr = get_by_url(
            url='{}/pulls/{}/files'.format(base_url, pr_id))
        for pr_file in files_from_pr:
            target_file_url = pr_file['raw_url']
            file_name = pr_file['filename']
            if file_name != f'lab_{lab_n}/main.py':  # Skip all files except main.py for the current lab
                continue

            source_hash = target_file_url.split('/')[-3]

            file_base_name = file_name.split('/')[1]  # expected: main.py
            to_url = os.path.join('tmp',
                                  '{}_{}.{}'.format(file_base_name.split('.')[0],
                                                    source_hash,
                                                    file_base_name.split('.')[1]))

            os.makedirs(os.path.dirname(to_url), exist_ok=True)

            download_file(from_url=target_file_url, to_url=to_url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get all changed files from pull requests')
    parser.add_argument('--lab', type=int, help='Lab to check')
    parser.add_argument('--current-pr', type=int, help='Current PR id')
    args: argparse.Namespace = parser.parse_args()
    print(args.current_pr)
    print(args.current_pr)
    print(args.current_pr)
    print(args.current_pr)
    main(args.lab, args.current_pr)
