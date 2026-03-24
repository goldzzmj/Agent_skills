import os
import sys

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import easyocr


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python ocr_image.py <image_path>")
    image_path = sys.argv[1]
    reader = easyocr.Reader(["ch_sim", "en"])
    res = reader.readtext(image_path, detail=1)
    for item in res:
        print(f"{item[1]}\t{item[0]}")
    print(f"count\t{len(res)}")


if __name__ == "__main__":
    main()
