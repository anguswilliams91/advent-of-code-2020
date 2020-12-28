"""25. RFID codes."""
C = 20201227


def find_loop_size(public_key: int) -> int:
    # find the loop size by brute force
    key = 1
    loop_size = 0
    while key != public_key:
        key = (key * 7) % C
        loop_size += 1

    return loop_size


def find_encryption_key(door_key: int, card_key: int) -> int:
    # find the encryption key implied by the door and card keys
    door_loop_size = find_loop_size(door_key)
    card_loop_size = find_loop_size(card_key)

    if door_loop_size < card_loop_size:
        subject_number = card_key
        loops = door_loop_size
    else:
        subject_number = door_key
        loops = card_loop_size

    encryption_key = 1
    for _ in range(loops):
        encryption_key = (encryption_key * subject_number) % C

    return encryption_key


if __name__ == "__main__":

    card_key = 2084668
    door_key = 3704642

    print(find_encryption_key(door_key, card_key))
