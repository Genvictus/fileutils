import os
import hashlib

from argparse import ArgumentParser

class DirHashes():
    def __init__(self, dir: str, hashes: dict[str, str]) -> None:
        self.dir = dir
        self.hashes = hashes

    def get_digests(dir: str):
        """
        Calculate the hashes of files in the directory,
        returning directories of relative path of the files in the directory
        with its hash in a dictionary
        """
        cwd = os.getcwd()
        try:
            os.chdir(dir)
            hashes: dict[str, str] = {}
            for path, _, filenames in os.walk('.'):
                for filename in filenames:
                    filepath = os.path.join(path, filename)
                    # calculate the hash
                    sha256_hash = hashlib.sha256()
                    with open(filepath,"rb") as f:
                        # Read and update hash string value in blocks of 4K
                        for byte_block in iter(lambda: f.read(4096),b""):
                            sha256_hash.update(byte_block)
                    hashes[filepath] = sha256_hash.hexdigest()
            return hashes
        except Exception as e:
            print(f'error while processing dir: {dir}: {e}')
        finally:
            os.chdir(cwd)

    def compare_hashes(self, dir_hashes_list: list["DirHashes"]):
        """
        Compare the hashes of the files in directories
        with hashes of other files in other dictionaries with the same relative path
        of their own respective dir as their roots

        (Practically comparing directories to directories with identical dir structure and files)
        """
        mismatch_hashes: dict[str, list[str]] = {}
        for dir_hashes in dir_hashes_list:
            for path, hash in dir_hashes.hashes.items():
                if hash != self.hashes[path]:
                    mismatch_hashes.setdefault(path, []).append(dir_hashes.dir)

        return mismatch_hashes

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('dir', nargs='*')

    args = parser.parse_args()
    dirs: list[str] = args.dir

    hashes_result: list[DirHashes] = [DirHashes(dir, DirHashes.get_digests(dir)) for dir in dirs]
    if len(hashes_result) > 1:
        primary_hashes = hashes_result.pop(0)
        mismatch_hashes = primary_hashes.compare_hashes(hashes_result)
        print(mismatch_hashes)
