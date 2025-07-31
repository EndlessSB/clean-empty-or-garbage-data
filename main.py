import os
import sys

debug = False

def is_junk_file(file_path):
    try:
        # Check file extension to skip non-text files (e.g., Excel, binary)
        _, ext = os.path.splitext(file_path)
        non_text_exts = {'.xls', '.xlsx', '.xlsm', '.xlsb', '.bin', '.exe', '.dll', '.zip', '.tar', '.gz', '.png', '.jpg', '.jpeg', '.pdf'}
        if ext.lower() in non_text_exts:
            return False  # Don't treat as junk, let user decide

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()
            # If file is empty or only whitespace, it's junk
            if not content:
                return True

            # If file is only a single word or a single line with no sentence structure, consider as junk
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if len(lines) == 1:
                # If it's a single word or just a few words, and not a sentence
                words = lines[0].split()
                if len(words) <= 3 and not any(p in lines[0] for p in '.!?'):
                    return True

            # If file has no sentence-ending punctuation, and is very short, consider as junk
            if len(content) < 30 and not any(p in content for p in '.!?'):
                return True

            # If file is only numbers or symbols, consider as junk
            if not any(c.isalpha() for c in content):
                return True

            # Otherwise, assume it's not junk
            return False
    except Exception as e:
        return True

def get_files(input_path):
    # Get all files in the given path (recursively if it's a directory)
    good_files = []
    junk_files = []
    if os.path.isfile(input_path):
        print("Error: Input path is a file")
        sys.exit(1)
    elif os.path.isdir(input_path):
        for root, dirs, filenames in os.walk(input_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                try:
                    if is_junk_file(file_path):
                        if debug == True:
                            print(f"[Debug] New junk File found: {file_path}")
                        junk_files.append(file_path)
                    else:
                        if debug == True:
                            print(f"[Debug] Non Junk File found: {file_path}")
                        good_files.append(file_path)
                except Exception as e:
                    # If file can't be read, consider it junk
                    junk_files.append(file_path)
    else:
        print(f"[Error] {input_path} is neither a file nor a directory")
        sys.exit(1)

    return good_files, junk_files

def delete_files(files):
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"[Error] A File's Deletion Failed: {e}")

if __name__ == "__main__":
    print("[NOTICE] This currently only supports text file formats.")
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"[Error] Input path {input_path} does not exist")
        sys.exit(1)

    if sys.argv[2]:
        if sys.argv[2] == "--debug":
            debug = True
    good_files, junk_files = get_files(input_path)

    print(f"[Info] Found {len(good_files)} good files and {len(junk_files)} junk files")

    delete = input("[Input] Do you want to delete the junk files? (y/n): ").lower()
    if delete == "y":
        delete_files(junk_files)
        print(f"[Info] Junk files deleted: {len(junk_files)}")
    else:
        print("[Info] Junk files not deleted")
