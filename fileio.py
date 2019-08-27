import os


def appendLine(filePath: str, string: str):
    """Append new line to a text file"""
    with open(filePath, 'a') as f:
        f.write(f'{string}\n')


def countLines(filePath: str):
    """Count the number of lines in a text file"""
    return sum(1 for _ in open(filePath))


def deleteLastLine(filePath: str):
    """Delete the last line from a text file"""
    with open(filePath, 'w') as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell() - 1
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
