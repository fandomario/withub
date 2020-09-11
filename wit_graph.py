import datetime
import distutils.core
from filecmp import dircmp
import os
import random
import shutil
import sys

from graphviz import Digraph


def init():
    try:
        os.mkdir('.wit')
    except FileExistsError as err:
        print(f"{err}")
    finally:
        path = os.path.join('.wit', 'images')
        path2 = os.path.join('.wit', 'staging_area')
        paths = (path, path2)
        for path in paths:
            os.makedirs(path, exist_ok=True)


def find_wit(path):
    which_dir_list = [path]
    parentpath = os.path.basename(os.getcwd())
    while parentpath != '':
        if '.wit' in os.listdir(os.getcwd()):
            return which_dir_list
        else:
            which_dir_list.append(parentpath)
            parentpath = os.path.basename(os.getcwd())
            os.chdir("..")
    raise ValueError("No wit")
    return False


def add(path):
    src = os.path.abspath(path)
    witlocation = find_wit(path)
    witlocation = witlocation[::-1]
    witdirectory = os.getcwd()
    dst = os.path.join(witdirectory, '.wit', 'staging_area')
    if os.path.isdir(src):
        for item in witlocation:
            dst = os.path.join(dst, item)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst)
    elif os.path.isfile(src):
        for item in witlocation[:-1]:
            dst = os.path.join(dst, item)
        shutil.copy(src, dst)


def is_wit_in_father():
    try:
        if find_wit(os.getcwd):
            pass
    except Exception:
        return False


def commit_id_creator():
    name = ""
    for _ in range(40):
        name += str(random.choice([random.randint(0, 9), chr(random.randint(97, 102))]))
    return name
 
 
def commit(MESSAGE):
    is_wit_in_father()
    apparent = 'None'
    commit_id_creator_name = commit_id_creator()
    commit_id_path = os.path.join('.wit', 'images', commit_id_creator_name)
    commit_id_txt_path = os.path.join('.wit', 'images', commit_id_creator_name + '.txt')
    if os.path.isfile(os.path.join('.wit', 'references.txt')):
        with open(os.path.join('.wit', 'references.txt'), 'r') as references_file:
            apparent = references_file.readline()[5:-1]
    with open(commit_id_txt_path, 'w') as commit_id_txt:
        commit_id_txt.write(f"parent={apparent}\ndate={datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y %Z')}\nmessage={sys.argv[2]}")
    src = os.path.join('.wit', 'staging_area')
    shutil.copytree(src, commit_id_path)
    reference_path = os.path.join('.wit', 'references' + '.txt')
    if not os.path.isdir(reference_path):
        with open(reference_path, 'w') as Reference_txt:
            Reference_txt.write(f"HEAD={commit_id_creator_name}\nMASTER={commit_id_creator_name}")


def status_files(dcmp):
    status_dict = {'Changes not staged for commit': [], 'Untracked files': [], 'Changes to be committed': []}
    for name in dcmp.diff_files:
        status_dict['Changes not staged for commit'].append(name)
    for left in dcmp.left_only:
        status_dict['Untracked files'].append(left)
    for right in dcmp.right_only:
        status_dict['Changes to be committed'].append(right)
    return status_dict


def status():
    is_wit_in_father()
    wit_path = os.getcwd()
    with open(os.path.join(wit_path, '.wit', 'references.txt'), 'r') as references_file:
        present_commit_id = references_file.readline()[5:-1]
    dcmp = dircmp(os.path.join(wit_path, ".wit", "images", present_commit_id), os.path.join(wit_path, ".wit", 'staging_area')) 
    status_dict = status_files(dcmp)
    dcmp = dircmp(wit_path, os.path.join(wit_path, ".wit", 'staging_area'), ignore=['.wit']) 
    status_dict = status_files(dcmp)
    reference_path = os.path.join('.wit', 'references' + '.txt')
    with open(reference_path, 'r') as commit_id:
        head = commit_id.readline()[5:-1]
        staging_area = os.listdir('C:\week10\Etztrubal\.wit\staging_area')
        head_directory = os.listdir(r'C:\week10\Etztrubal\.wit\images\\' + head)
        difference = set(staging_area).symmetric_difference(set(head_directory))
        print(f"commit id: {head}\n"
        f"Changes to be committed:{difference}\n"
        f"Changes not staged for commit: {status_dict['Changes not staged for commit']}\n"
        f"Untracked files: {status_dict['Untracked files']}"
        )
    return status_dict


def checkout(commit_id):
    is_wit_in_father()
    wit_path = os.getcwd()
    status_dict = status()
    if commit_id == 'master':
        with open(os.path.join(wit_path, '.wit', 'references.txt'), 'r') as references_file:
            master_commit_id = references_file.readlines()
        commit_id = master_commit_id[1][7:-1]
    if len(status_dict['Changes to be committed']) < 1 or len(status_dict['Changes not staged for commit']) < 1:
        src = os.path.join(wit_path, '.wit', 'images', commit_id)
        dst = wit_path
        distutils.dir_util.copy_tree(src, dst, preserve_mode=0)
    else:
        return "Checkout did not run"
    with open(os.path.join(wit_path, '.wit', 'references.txt'), 'r') as references_file:
        lines = references_file.readlines()
    lines[0] = f'HEAD={commit_id}\n'
    with open(os.path.join(wit_path, '.wit', 'references.txt'), 'w+') as references_file:
        references_file.writelines(lines)
    src = os.path.join(wit_path, '.wit', 'images', commit_id)
    dst = os.path.join(wit_path, '.wit', 'staging_area')
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)


def graph():
    is_wit_in_father()
    wit_path = os.getcwd()
    graph = Digraph('G', filename='something', format='png')
    with open(os.path.join(wit_path, '.wit', 'references.txt'), 'r') as references_file:
        lines = references_file.readlines()
    parent_line = lines[0][5:-1] + '.txt'
    while parent_line != 'None':
        with open(os.path.join(wit_path, '.wit', 'images', parent_line), 'r') as images_file:
            lines = images_file.readlines()
        new_parent_line = lines[0][7:-1]
        if new_parent_line != 'None':
            new_parent_line += '.txt'
            graph.edge(parent_line[0:40], new_parent_line[0:40])
        parent_line = new_parent_line
    graph.view()


if __name__ == "__main__":
    if sys.argv[1] == 'init':
        init()
    if sys.argv[1] == 'add':
        add(sys.argv[2])
    if sys.argv[1] == 'commit':
        commit(sys.argv[2])
    if sys.argv[1] == 'status':
        status()
    if sys.argv[1] == 'checkout':
        checkout(sys.argv[2])
    if sys.argv[1] == 'graph':
        graph()