from textnode import TextType, TextNode
import os, shutil, sys
from htmlnode import generate_page

STATIC_DIR_LOC = 'static'
PUBLIC_DIR_LOC = 'public'
CONTENT_DIR_LOC = 'content'

def copy_from_static():
    if not os.path.exists(STATIC_DIR_LOC):
        print(f"{STATIC_DIR_LOC} doesn't exist")
        return

    if os.path.exists(PUBLIC_DIR_LOC):
        print(f"Removing all files from {PUBLIC_DIR_LOC}")
        shutil.rmtree(PUBLIC_DIR_LOC)
    os.mkdir(PUBLIC_DIR_LOC)

    static_files = os.listdir(STATIC_DIR_LOC)
    while static_files:
        file = static_files.pop()
        static_dir_file_loc = os.path.join(STATIC_DIR_LOC, file)
        public_dir_file_loc = os.path.join(PUBLIC_DIR_LOC, file)
        if os.path.isfile(static_dir_file_loc):
            print(f"Moving {file} to {PUBLIC_DIR_LOC}")
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
    if len(sys.argv) >= 2:
        base_url = sys.argv[1]
    copy_from_static()
    generate_pages_recursive(CONTENT_DIR_LOC, 'template.html', PUBLIC_DIR_LOC, base_url)


if __name__ == "__main__":
    main()
