import os

import docx
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from agent_utils import get_model


class FileSurferState(BaseModel):
    current_dir: str = os.getcwd()


class FileSurferAgent(Agent[FileSurferState, str]):
    def __init__(self, model_name: str = 'openai:gpt-4o-mini', system_prompt: str = ""):
        # Initialize FileSurferState
        file_surfer_state = FileSurferState()
        self.name = "FileSurferAgent"
        # Call the parent constructor
        active_model = get_model()

        super().__init__(
            model=active_model,
            deps_type=FileSurferState,
            result_type=str,
            system_prompt=system_prompt or (
                "A helpful assistant with access to the file system. Ask them to list files, change directories, "
                "read file contents, and save new files."
            ),
        )


def create_filesurfer_agent() -> FileSurferAgent:
    file_surfer = FileSurferAgent()

    @file_surfer.tool
    async def get_current_dir(ctx: RunContext[FileSurferState]) -> str:
        """
        Get the current working directory.

        This function returns the current directory path where the agent is operating.

        Returns:
            str: The current working directory path.
        """
        print("get_current_dir called")
        return ctx.deps.current_dir

    @file_surfer.tool
    async def list_files(ctx: RunContext[FileSurferState]) -> str:
        """
        List all files in the current directory.

        This function scans the current directory and returns a list of all files.
        It excludes directories and only includes regular files.

        Returns:
            str: A newline-separated string of filenames, or a message indicating no files were found.
        """
        print("list_files called")
        files = [f for f in os.listdir(ctx.deps.current_dir) if os.path.isfile(os.path.join(ctx.deps.current_dir, f))]

        rv = "\n".join(files) or "No files found in the current directory."
        print(rv)
        return rv

    @file_surfer.tool
    async def change_dir(ctx: RunContext[FileSurferState], path: str) -> str:
        """
        Change the current directory.

        This function attempts to change the current working directory to the specified path.
        If successful, it updates the current directory state. If the path is invalid or inaccessible,
        it returns an error message.

        Args:
            path (str): The target directory path to change to.

        Returns:
            str: A message indicating the result of the directory change operation.
        """
        print(f"change_dir called with path: {path}")
        try:
            os.chdir(path)
            ctx.deps.current_dir = os.getcwd()
            return f"Changed directory to {ctx.deps.current_dir}"
        except Exception as e:
            return f"Failed to change directory: {str(e)}"

    @file_surfer.tool
    async def list_dirs(ctx: RunContext[FileSurferState]) -> str:
        """
        List all directories in the current directory.

        This function scans the current directory and returns a list of all subdirectories.
        It excludes regular files and only includes directories.

        Returns:
            str: A newline-separated string of directory names, or a message indicating no directories were found.
        """
        print("list_dirs called")
        dirs = [d for d in os.listdir(ctx.deps.current_dir) if os.path.isdir(os.path.join(ctx.deps.current_dir, d))]
        return "\n".join(dirs) or "No directories found in the current directory."

    @file_surfer.tool
    async def get_file_contents(ctx: RunContext[FileSurferState], filename: str) -> str:
        """
        Get the contents of a file.

        This function reads the contents of a specified file and returns it as a string.
        It supports reading from .txt, .md, and .docx files. For unsupported file types,
        it returns an error message.

        Args:
            filename (str): The name of the file to read.

        Returns:
            str: The contents of the file, or an error message if the file cannot be read.
        """
        print(f"get_file_contents called with filename: {filename}")
        print(f"save_to_new_file called with filename: {filename}")
        file_path = os.path.join(ctx.deps.current_dir, filename)
        try:
            if filename.endswith('.txt') or filename.endswith('.md'):
                with open(file_path, 'r') as file:
                    return file.read()
            elif filename.endswith('.docx'):
                doc = docx.Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            else:
                return "Unsupported file type."
        except Exception as e:
            return f"Failed to read file: {str(e)}"

    @file_surfer.tool
    async def save_to_new_file(ctx: RunContext[FileSurferState], filename: str, content: str) -> str:
        """
        Save content to a new file.

        This function writes the provided content to a new file with the specified filename.
        If a file with the same name already exists, it returns an error message. Otherwise,
        it saves the content and confirms the operation.

        Args:
            filename (str): The name of the file to create.
            content (str): The content to write to the file.

        Returns:
            str: A message indicating the result of the save operation.
        """
        file_path = os.path.join(ctx.deps.current_dir, filename)
        if os.path.exists(file_path):
            return "File already exists. Choose a different filename."
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return f"File saved successfully as {filename}"
        except Exception as e:
            return f"Failed to save file: {str(e)}"

    @file_surfer.tool
    async def delete_file(ctx: RunContext[FileSurferState], filename: str, confirm: str = "No") -> str:
        """
        Delete a file.

        This function attempts to delete the specified file. If the file exists and is successfully
        deleted, it returns a confirmation message. If the file does not exist or cannot be deleted,
        it returns an error message.

        Args:
            filename (str): The name of the file to delete.
            confirm (str): User confirmation is done or not - Yes / No
        Returns:
            str: A message indicating the result of the delete operation.

        """
        print(f"delete_file called with filename: {filename}")
        print(f"confirm: {confirm}")
        if confirm.lower() != "yes":
            return "File not deleted. Please confirm with 'Yes' from the user."

        file_path = os.path.join(ctx.deps.current_dir, filename)
        if not os.path.exists(file_path):
            return "File does not exist."
        try:
            os.remove(file_path)
            return f"File {filename} deleted successfully."
        except Exception as e:
            return f"Failed to delete file: {str(e)}"
    return file_surfer

