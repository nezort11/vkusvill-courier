from subprocess import run

CMD = """
on run argv
  display notification (item 2 of argv) with title (item 1 of argv) sound name "default"
end run
"""


def notify(title, text):
    result = run(['osascript', '-e', CMD, title, text])
    result.check_returncode()


if __name__ == "__main__":
    notify("Test", "Hello, World!")
