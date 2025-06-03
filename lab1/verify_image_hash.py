import hashlib


def verify_image_hash(image_path: str, given_hash: str) -> bool:
    """Verify SHA-1 hash of the image against the expected value."""
    try:
        with open(image_path, 'rb') as f:
            computed_hash = hashlib.sha1(f.read()).hexdigest()
        if computed_hash == given_hash:
            print('Bitstream image verified successfully.')
            return True
        else:
            print('Error: Bitstream image verification failed.')
            return False
    except IOError as e:
        print(f"Error opening file: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
