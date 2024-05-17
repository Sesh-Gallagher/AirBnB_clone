#!/usr/bin/python3
""" Module that Initializes the package."""

from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
