import json
import csv


def import_json(file_path):
    with open(file_path, "r") as file:
        body = json.load(file)
        return f"{body}"


def import_csv(file_path):
    with open(file_path, "r") as file:
        body = csv.reader(file)
        output = []
        for line in body:
            output.append(line)
        return f"{output}"


note_cache = {}


def cache_notes(id, value):
    cache = {id: value}
    note_cache.update(cache)
