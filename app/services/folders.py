from app.db import sessionlocal
from app.models import Folder, Note
from random import choice
import itertools


def unique_folder_name(db=sessionlocal()):
    infinite_counter = itertools.count(start=1)
    for counter in infinite_counter:
        folder = f"Folder.{str(counter)}"
        test = db.query(Folder).filter(Folder.folder_name == folder).first()
        if test is None:
            return folder


def eligible_folders(db=sessionlocal()):
    range_of_folders = (
        db.query(Folder.folder_name).filter(Folder.amount_of_notes < 10).all()
    )
    if range_of_folders:
        eligible = [counter[0] for counter in range_of_folders]
        folder = choice(eligible)
        return folder
    else:
        return "False"


def get_folder(folder_name_, title_, db=sessionlocal()):
    if folder_name_ != "None":
        if folder_name_.strip() == "":
            return "Empty input"
        test_folder = (
            db.query(Folder).filter(Folder.folder_name == folder_name_).first()
        )
        if test_folder:
            length = test_folder.amount_of_notes
            test_title = (
                db.query(Note)
                .filter(Note.folder_name == folder_name_, Note.title == title_)
                .first()
            )
            if length >= 10:
                return "length issue"
            elif test_title:
                return "name clash"
            else:
                return folder_name_
        elif test_folder is None:
            return "folder name does not exist"
    assigned_folder = eligible_folders()
    if folder_name_ == "None" and assigned_folder != "False":
        return f"{assigned_folder}"
    if folder_name_ == "None" and assigned_folder == "False":
        _folder_ = unique_folder_name()
        return _folder_


def cache_folders():
    pass
