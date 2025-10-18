from textnode import TextType, TextNode
import os, shutil, sys
from htmlnode import generate_page

STATIC_DIR_LOC = 'static'
PUBLIC_DIR_LOC = 'public'
CONTENT_DIR_LOC = 'content'
DOC_DIR_LOC = 'docs'

def copy_from_static(target_dir):
    if not os.path.exists(STATIC_DIR_LOC):
        print(f"{STATIC_DIR_LOC} doesn't exist")
        return

    if os.path.exists(target_dir):
        print(f"Removing all files from {target_dir}")
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)

    static_files = os.listdir(STATIC_DIR_LOC)
    while static_files:
        file = static_files.pop()
        static_dir_file_loc = os.path.join(STATIC_DIR_LOC, file)
        public_dir_file_loc = os.path.join(target_dir, file)
        if os.path.isfile(static_dir_file_loc):
            print(f"Moving {file} to {target_dir}")
            shutil.copy(static_dir_file_loc, public_dir_file_loc)
        else:
            print(f"Creating dir: {file}")
            os.mkdir(public_dir_file_loc)
            static_files.extend(map(lambda x: os.path.join(file, x), os.listdir(static_dir_file_loc)))
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_url):
    if not os.path.exists(dir_path_content):
        print(f"{dir_path_content} doesn't exist")
        return

    content_files = os.listdir(dir_path_content)
    while content_files:
        file = content_files.pop()
        content_dir_file_loc = os.path.join(dir_path_content, file)
        public_dir_file_loc = os.path.join(dest_dir_path, file)
        if os.path.isfile(content_dir_file_loc):
            generate_page(content_dir_file_loc, template_path, public_dir_file_loc[:public_dir_file_loc.rfind('.')]+'.html', base_url)
        else:
            content_files.extend(map(lambda x: os.path.join(file, x), os.listdir(content_dir_file_loc)))

def main():
    base_url = '/'
    target_dir = PUBLIC_DIR_LOC
    if len(sys.argv) >= 2:
        base_url = sys.argv[1]
    if len(sys.argv) >= 3:
        target_dir = sys.argv[2]
    copy_from_static(target_dir)
    generate_pages_recursive(CONTENT_DIR_LOC, 'template.html', target_dir, base_url)


if __name__ == "__main__":
    main()
