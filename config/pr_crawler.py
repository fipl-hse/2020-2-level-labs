# pylint: skip-file
"""
Download all files from opened pull request
"""

import os
import sys
import urllib3
import argparse

from requests import get

TOKEN = '5819289b9c5f7969989a36ab7deb360deeca8ac2'


def get_by_url(url: str):
    headers = {'Authorization': f'token {TOKEN}'}
    response = get(url, headers=headers)
    content = response.json()
    return content


def download_file(from_url: str, to_url: str):
    http = urllib3.PoolManager()
    req = http.request('GET', from_url, preload_content=False)

    with open(to_url, 'wb') as out:
        while True:
            data = req.read(100)
            if not data:
                break
            out.write(data)
    req.release_conn()


def main(lab_n: int):
    if 'TRAVIS_COMMIT' not in os.environ:
        print('Need proper environment variables')
        sys.exit(1)

    current_commit_hash = os.environ.get('TRAVIS_COMMIT', 'None')

    base_url = 'https://api.github.com/repos/fipl-hse/2020-2-level-labs'

    content = get_by_url(url='{}/pulls?state=all'.format(base_url))
    for pull_req in content:
        pr_id = pull_req['number']
        files_from_pr = get_by_url(
            url='{}/pulls/{}/files'.format(base_url, pr_id))
        for pr_file in files_from_pr:
            target_file_url = pr_file['raw_url']
            file_name = pr_file['filename']
            if file_name != f'lab_{lab_n}/main.py':  # Skip all files except main.py for the current lab
                continue
            source_hash = target_file_url.split('/')[-3]

            print(source_hash, current_commit_hash)
            if source_hash == current_commit_hash:
                print('Ignoring file: {}'.format(file_name))
                continue
            print(file_name)
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
    args: argparse.Namespace = parser.parse_args()
    main(args.lab)

