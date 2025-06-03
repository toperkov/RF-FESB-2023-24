import hashlib
from pathlib import Path
from lab1.verify_image_hash import verify_image_hash


def test_verify_image_hash_matches(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    content = b"sample data"
    file_path.write_bytes(content)
    expected_hash = hashlib.sha1(content).hexdigest()
    assert verify_image_hash(str(file_path), expected_hash) is True


def test_verify_image_hash_mismatch(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_bytes(b"other data")
    wrong_hash = hashlib.sha1(b"different").hexdigest()
    assert verify_image_hash(str(file_path), wrong_hash) is False
