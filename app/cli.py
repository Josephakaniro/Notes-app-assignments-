import typer
import os
from app.db import init_DB, sessionlocal
from app.models import Folder, Note, Format
from app.services.folders import get_folder
from app.services.notes import cache_notes, import_csv, import_json
from tabulate import tabulate


app = typer.Typer()


@app.command()
def new_folder(
    folder_name: str = typer.Option(..., help="Enter folder name", prompt=True),
    tag: str = typer.Option("None", help="Enter folder tag (optional)", prompt=True),
):
    """Create a new folder"""

    init_DB()
    db = sessionlocal()
    try:
        existing_folder = (
            db.query(Folder).filter(Folder.folder_name == folder_name).first()
        )
        if existing_folder:
            typer.echo(
                f"Folder '{folder_name}' already exists. Please choose a different name."
            )
            return
        folder = Folder(folder_name=folder_name, amount_of_notes=0, tag=tag)
        db.add(folder)
        db.commit()
        typer.echo(f"'{folder_name}' created successfully.")
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def new_note(
    title: str = typer.Option(..., help="Enter note title", prompt=True),
    folder_name: str = typer.Option("None", help="Enter folder name", prompt=True),
    body: str = typer.Option(..., help="Body of the note", prompt=True),
):
    """Create a new note"""
    init_DB()
    db = sessionlocal()
    try:
        the_folder_of_use = get_folder(folder_name_=folder_name, title_=title)
        if the_folder_of_use == "Empty input":
            typer.echo(f"Empty input")
            return
        if the_folder_of_use == "length issue":
            typer.echo(f"'{folder_name}' folder has up to 10 notes")
            return
        if the_folder_of_use == "name clash":
            typer.echo(f"'{title}' is already found within {folder_name}")
            return
        if the_folder_of_use == "folder name does not exist":
            typer.echo(f"'{folder_name}' does not exist")
            return

        item = db.query(Folder).filter(Folder.folder_name == the_folder_of_use).first()
        if item:
            item.amount_of_notes += 1
        else:
            folder = Folder(folder_name=the_folder_of_use, amount_of_notes=1)
            db.add(folder)

        note = Note(
            title=title,
            folder_name=the_folder_of_use,
            body=body,
            format=Format.TEXT,
        )
        db.add(note)
        db.commit()
        cache_notes(id=note.id, value=note.body)
        typer.echo(f"Note '{note.title}' created successfully in '{note.folder_name}'.")
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def delete_note(
    folder_name: str = typer.Option(..., help="Enter folder name", prompt=True),
    title: str = typer.Option(..., help="Enter note title", prompt=True),
):
    """Delete a note"""
    init_DB()
    db = sessionlocal()
    try:
        note = (
            db.query(Note)
            .filter(Note.folder_name == folder_name, Note.title == title)
            .first()
        )

        if note:
            folder = (
                db.query(Folder)
                .filter(Folder.folder_name == f"{note.folder_name}")
                .first()
            )
            folder.amount_of_notes -= 1
            db.delete(note)
            db.commit()
            typer.echo(f"You have successfully deleted '{title}' from '{folder_name}'")
        else:
            typer.echo(f"There is no note named '{title}' in '{folder_name}'")
            return
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def delete_folder(
    folder_name: str = typer.Option(..., help="Enter folder name", prompt=True),
):
    """Delete a folder"""
    init_DB()
    db = sessionlocal()
    try:
        folder = db.query(Folder).filter(Folder.folder_name == folder_name).first()
        if folder:
            db.query(Note).filter(Note.folder_name == folder_name).delete()
            db.delete(folder)
            db.commit()
            typer.echo(f"You have successfully deleted '{folder_name}'")
        else:
            typer.echo(f"There is no folder named '{folder_name}'")
            return
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def import_csv_notes(
    title: str = typer.Option(..., help="Name of file", prompt=True),
    folder_name: str = typer.Option("None", help="Enter folder name", prompt=True),
    file_path: str = typer.Option(..., help="CSV file path to import", prompt=True),
):
    """import .csv file"""
    init_DB()
    db = sessionlocal()
    try:
        if os.path.isfile(file_path):
            _body = import_csv(file_path)
        else:
            typer.echo(f"'{file_path}' does not exist")
            return

        the_folder_of_use = get_folder(folder_name_=folder_name, title_=title)
        if the_folder_of_use == "Empty input":
            typer.echo(f"Empty input")
            return
        if the_folder_of_use == "length issue":
            typer.echo(f"'{folder_name}' folder has up to 10 notes")
            return
        if the_folder_of_use == "name clash":
            typer.echo(f"'{title}' is already found within {folder_name}")
            return
        if the_folder_of_use == "folder name does not exist":
            typer.echo(f"'{folder_name}' does not exist")
            return
        item = db.query(Folder).filter(Folder.folder_name == the_folder_of_use).first()
        if item:
            item.amount_of_notes += 1
        else:
            folder = Folder(folder_name=the_folder_of_use, amount_of_notes=1)
            db.add(folder)

        note = Note(
            title=title,
            folder_name=the_folder_of_use,
            body=_body,
            format=Format.CSV,
        )
        db.add(note)
        db.commit()
        cache_notes(id=note.id, value=note.body)
        typer.echo(f"Note '{note.title}' created successfully in '{note.folder_name}'.")
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def import_json_notes(
    title: str = typer.Option(..., help="Name of file", prompt=True),
    folder_name: str = typer.Option("None", help="Enter folder name", prompt=True),
    file_path: str = typer.Option(..., help="CSV file path to import", prompt=True),
):
    """import .json file"""
    init_DB()
    db = sessionlocal()
    try:
        if os.path.isfile(file_path):
            _body = import_json(file_path)
        else:
            typer.echo(f"'{file_path}' does not exist")
            return

        the_folder_of_use = get_folder(folder_name_=folder_name, title_=title)
        if the_folder_of_use == "Empty input":
            typer.echo(f"Empty input")
            return
        if the_folder_of_use == "length issue":
            typer.echo(f"'{folder_name}' folder has up to 10 notes")
            return
        if the_folder_of_use == "name clash":
            typer.echo(f"'{title}' is already found within {folder_name}")
            return
        if the_folder_of_use == "folder name does not exist":
            typer.echo(f"'{folder_name}' does not exist")
            return
        item = db.query(Folder).filter(Folder.folder_name == the_folder_of_use).first()
        if item:
            item.amount_of_notes += 1
        else:
            folder = Folder(folder_name=the_folder_of_use, amount_of_notes=1)
            db.add(folder)

        note = Note(
            title=title,
            folder_name=the_folder_of_use,
            body=_body,
            format=Format.JSON,
        )
        db.add(note)
        db.commit()
        cache_notes(id=note.id, value=note.body)
        typer.echo(f"Note '{note.title}' created successfully in '{note.folder_name}'.")
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def search(title: str = typer.Option(..., help="Name of the note", prompt=True)):
    """Search for a Note"""
    init_DB()
    db = sessionlocal()
    try:
        search_results = db.query(Note).filter(Note.title == title).all()

        if search_results is None:
            typer.echo(f" There is no Note named '{title}'")
            return
        if len(search_results) == 1:
            typer.echo(f"{search_results[0].body}")
            return

        typer.echo(f"{len(search_results)} different notes have the title {title}:")
        for i, counter in enumerate(search_results, start=1):
            typer.echo(f"{i}. '{counter.title}' in '{counter.folder_name}'")

        choice = typer.prompt(
            f"Enter the number of the note you want (1-{len(search_results)})"
        )
        index = int(choice) - 1
        selected_choice = search_results[index]
        typer.echo(
            f"You selected '{selected_choice.title}' in '{selected_choice.folder_name}'"
        )
        typer.echo(f"{selected_choice.body}")
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def folder_analytics():
    """Folder analytics"""
    init_DB()
    db = sessionlocal()
    try:
        Folders = db.query(Folder).all()
        data = []
        for object in Folders:
            collection = (
                f"{object.folder_name}",
                f"{object.amount_of_notes}",
                f"{object.tag}",
            )
            data.append(collection)
        typer.echo(
            tabulate(
                data,
                headers=["Folder name", "Amount of Notes", "Tags"],
                tablefmt="simple_grid",
            )
        )
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()


@app.command()
def note_analytics():
    """Note analytics"""
    init_DB()
    db = sessionlocal()
    try:
        Notes = db.query(Note).all()
        data = []
        for object in Notes:
            collection = (
                f"{object.title}",
                f"{object.folder_name}",
                f"{object.body}",
                f"{object.format}",
            )
            data.append(collection)
        typer.echo(
            tabulate(
                data,
                headers=["Title", "Folder name", "content", "format"],
                tablefmt="simple_grid",
            )
        )
    except Exception as e:
        db.rollback()
        typer.echo(f"An error occurred: {e}")
    finally:
        db.close()
