import sys
import pathlib

test = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

def hash_string(s:str):
    current = 0
    for c in s:
        current = (current + ord(c)) * 17
        current %= 256
    return current

def find_box(box: list, label: str):
    for i, (label_, _) in enumerate(box):
        if label == label_:
            return i
    return None

def main(argv=None):
    if argv is None:
        argv = sys.argv[:]

    line = open(pathlib.Path(__file__).parent / "input").readline().rstrip("\n")
    # line = test

    items = line.split(",")
    s = sum(hash_string(item) for item in items)
    print("Part 1:", s)

    boxes = [[] for _ in range(256)]
    for item in items:
        if "=" in item:
            label, focal_length = item.split("=")
            box_id = hash_string(label)
            box = boxes[box_id]
            if (slot_number := find_box(box, label)) is not None:
                box[slot_number] = (label, focal_length)
            else:
                box.append((label, focal_length))
        elif item.endswith("-"):
            label = item[:-1]
            box_id = hash_string(label)
            box = boxes[box_id]
            if (slot_number := find_box(box, label)) is not None:
                box.pop(slot_number)

    s = 0
    for box_number, box in enumerate(boxes):
        for slot_number, (_, focal_length) in enumerate(box):
            s += (box_number + 1) * (slot_number + 1) * int(focal_length)
    print(s)

if __name__ == "__main__":
    main()