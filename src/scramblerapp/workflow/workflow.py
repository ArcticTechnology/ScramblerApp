import getpass
import pathlib
import re
from typing import Type, Union

from cmd2.string_utils import strip_quotes

from ..dircrawler.filemodder import FileModder


class Workflow:

    def __init__(self, menu_instance):
        self.menu = menu_instance
        self.encrypt: bool = self.menu.encrypt
        self.keyword: str = 'Encrypt' if self.encrypt else 'Decrypt'

    def validate_password(self) -> str:
        done: bool = False
        attempts: int = 0
        max_attempts: int = 1
        while not done and attempts <= max_attempts:
            prompt_msg = 'Password (>10 chars required): ' if self.encrypt else 'Decryption Password: '
            pwd = getpass.getpass(prompt_msg)

            if not pwd:
                pwd = ''

            if self.encrypt and len(pwd) <= 10:
                self.menu.perror(
                    'Error: Password must be strictly greater than 10 characters.'
                )
                attempts += 1

            elif self.encrypt:
                confirm_pwd = getpass.getpass('Confirm Password: ')
                if pwd != confirm_pwd:
                    self.menu.perror(
                        'Error: Passwords do not match. Please try again.')
                    attempts += 1

                    # Reset password if they do not match.
                    pwd = ''
                else:
                    done = True

            elif not self.encrypt:
                if pwd:
                    done = True
                else:
                    self.menu.perror('Error: Password cannot be empty')
                    attempts += 1

        return pwd

    def get_password(self) -> str:
        password: str = self.validate_password()
        if password:
            return password
        else:
            self.menu.perror('Operation cancelled due to password failure.')
            return ''

    def print_option_title(self):
        self.menu.poutput(f'=== {self.keyword} ===')
        self.menu.poutput()

    def print_option_heading(self, question_prefix: str):
        self.print_option_title()
        self.menu.poutput(f'{question_prefix} {self.keyword.lower()}?')
        self.menu.poutput()


class FileCryptoWorkflow(Workflow):

    def __init__(self, menu_instance, resource_type: str,
                 working_directory: pathlib.Path):
        super().__init__(menu_instance)

        # Type of resource to handle: 'file', 'directory'.
        self.resource_type: str = resource_type
        self.working_directory: pathlib.Path = working_directory
        self.naked = True if (not self.encrypt
                              and self.resource_type == 'file') else False

    def show_note_and_get_prompt(self, note: str, prompt: str) -> str:
        self.menu.poutput(note)
        self.menu.poutput()
        value: str = self.menu.read_input(prompt).strip()
        self.menu.poutput()

        return value

    def get_destination_files_suffix(self) -> dict[list[str]]:
        prefix: str = f'[NOTE]: By default, {self.keyword.lower()} will create {"a new file" if self.resource_type == "file" else "new files"} with "'
        suffix: str = '" at the end. You may change this suffix.'
        notice_prompt: str = ''.join([
            prefix, '-', self.menu.instance.encrypted_file_suffix if
            self.encrypt else self.menu.instance.decrypted_file_suffix, suffix
        ])

        destination_file_suffix: str = self.menu.instance.clean_file_suffix(
            self.show_note_and_get_prompt(
                notice_prompt, 'Specify a different suffix [Optional]: '))

        encrypt_suffix: str = self.menu.instance.encrypted_file_suffix
        decrypt_suffix: str = self.menu.instance.decrypted_file_suffix

        if destination_file_suffix:
            if self.encrypt:
                encrypt_suffix = destination_file_suffix
            else:
                decrypt_suffix = destination_file_suffix

        return {
            'encrypt': [encrypt_suffix],
            'decrypt': [
                decrypt_suffix,
                decrypt_suffix,
            ],
        }

    def filter_source_files_by_extension(self):
        notice_prompt: str = f'[NOTE]: By default, this {self.keyword.lower()}s files with the ".txt" extension. You may change this to a different extension. Use "*" to decrypt all files regardless of extension (this can be dangerous).'
        raw_extension: str = self.show_note_and_get_prompt(
            notice_prompt, 'Specify a file type [Optional]: ')

        return FileModder.format_ext(raw_extension)

    def filter_source_files_by_directory_depth(self) -> int:
        notice_prompt: str = f'[NOTE]: By default, this {self.keyword.lower()}s files 1 subdirectory down from your root directory. You may change this to a depth of 0 to 3.'
        depth_int: int = 1
        depth: str = self.show_note_and_get_prompt(
            notice_prompt, 'Specify a depth [Optional]: ')

        try:
            if not depth:
                depth_int

            depth_int = int(depth)
            if depth_int < 0 or depth_int > 3:
                raise ValueError
        except ValueError as e:
            depth_int = 1
            self.menu.pwarning(
                f'[NOTE]: Using default depth of {depth_int} as directory depth'
            )
            self.menu.poutput()

        return depth_int

    def keep_original_files(self) -> bool | None:
        resource_name: str = 'file' if self.resource_type == 'file' else 'files'
        delete_original_files: str = self.menu.read_input(
            f'Type D to delete the original {resource_name} [Optional]: '
        ).strip()

        self.menu.poutput()

        keep_orig: bool = True
        if delete_original_files in ['D']:
            delete_original_files = self.menu.read_input(
                f'Are you sure you want to {self.keyword.lower()} the {resource_name} and DELETE the original (Y/n)? '
            ).strip()
            if delete_original_files in ['Y']:
                keep_orig = False
            elif delete_original_files in ['n']:
                keep_orig = True
            else:
                self.menu.perror('Operation cancelled, please input Y or n.')
                return None
        else:
            preserve_original_files = self.menu.read_input(
                f'Are you sure you want to {self.keyword.lower()} the {resource_name} and KEEP the original (Y/n)? '
            ).strip()
            if preserve_original_files in ['Y']:
                keep_orig = True
            elif preserve_original_files in ['n']:
                keep_orig = False
            else:
                self.menu.perror('Operation cancelled, please input Y or n.')
                return None

        self.menu.poutput()

        return keep_orig

    def show_directory_confirmation(self, dir_path: str):
        self.menu._clear_terminal()
        self.print_option_title()
        self.menu.pwarning(
            f'Warning: You are about to {self.keyword.lower()} all files in the following directory and its subdirectories:'
        )
        self.menu.poutput()
        self.menu.poutput(f'{dir_path}')
        self.menu.poutput()

    def start(self, args: str, selectable_directory: bool = False):
        # args contains the file or directory path.
        path: str = args.strip() if args else ''

        if self.resource_type == 'directory' and not selectable_directory:
            path = self.working_directory
        else:
            self.print_option_heading(
                question_prefix=f'Which {self.resource_type} do you want to')

            if not path:
                self.menu.pwarning('Press <TAB> to browse.')
                self.menu.poutput()
                try:
                    # Interactive prompt.
                    path = self.menu.read_input(prompt='> ',
                                                completer=self.complete)

                    # cmd2 automatically adds quotes to the prompt when using
                    # the tab autocompletion feature. If a file or directory,
                    # in any place below the current one contains a space, it adds
                    # a `"` quote; if a file contains `"` inside the name, cmd2
                    # uses `'` as quote instead. This quote is added to the prompt
                    # and passed as raw path. The only clean and simple cases
                    # is with standard file names.
                    path = path.strip()
                    old_path: str = path
                    path = strip_quotes(path)
                    # If unbalanced quotes, remove the first quote manually.
                    if path and path == old_path and path[0] in ['"', "'"]:
                        path = path[1:]
                except (EOFError, KeyboardInterrupt):
                    self.menu.perror('\nAborted.')
                    return False

            self.menu.poutput()

            if not path:
                self.menu.perror(
                    f"Error: Specify a valid path. Press TAB to browse.")
                return False

        p_path: pathlib.Path = pathlib.Path(path).expanduser().resolve()

        if not p_path.exists():
            self.menu.perror(f'Error: Path "{p_path}" does not exists.')
            return False

        password: str
        if self.resource_type == 'file':
            if p_path.is_dir():
                self.menu.perror(
                    f'"{p_path}" is a directory. Select a file instead.')
                return False
            elif p_path.is_file():
                crypto_file_extensions = self.get_destination_files_suffix()

                keep_orig: bool = self.keep_original_files()
                if keep_orig is None:
                    return False

                password = self.get_password()
                if not password:
                    return False

                result = self.menu.scrambler.encrypt_file(
                    password,
                    str(p_path),
                    decrypt=not self.encrypt,
                    keep_org=keep_orig,
                    naked=self.naked,
                    tag_options=crypto_file_extensions,
                )

                self.menu._clear_terminal()
                self.print_option_title()
                if result['status'] == 200:
                    self.menu.psuccess('Operation completed.')
                    self.menu.poutput()
                    self.menu.poutput(result['message'])
                else:
                    self.menu.perror('Error.')
                    self.menu.poutput()
                    self.menu.poutput(result['message'])

        elif self.resource_type == 'directory':
            if p_path.is_file():
                self.menu.perror(
                    f'"{p_path}" is a file. Select a directory instead.')
                return False
            elif p_path.is_dir():
                self.show_directory_confirmation(p_path)
                crypto_file_extensions = self.get_destination_files_suffix()
                extension = self.filter_source_files_by_extension()
                depth: int = self.filter_source_files_by_directory_depth()
                keep_orig: bool = self.keep_original_files()
                if keep_orig is None:
                    return False

                password = self.get_password()
                if not password:
                    return False

                self.menu._clear_terminal()
                self.print_option_title()
                # tqdm shows progress here.

                # Mock:
                #   result = {'status': 200, 'message': 'OK', 'output': ['ok 0', 'ok 1']}
                result = self.menu.scrambler.encrypt_all_files(
                    password,
                    str(p_path),
                    decrypt=not self.encrypt,
                    extension=extension,
                    keep_org=keep_orig,
                    naked=self.naked,
                    tag_options=crypto_file_extensions,
                    depth=depth,
                )

                self.menu._clear_terminal()
                self.print_option_title()
                if result['status'] == 200:
                    for out in result['output']:
                        self.menu.poutput(out)
                        self.menu.poutput()
                    self.menu.poutput('Operation completed.')
                else:
                    self.menu.perror('Error.')
                    self.menu.poutput()
                    self.menu.poutput(result['message'])
        else:
            self.menu.perror(
                f'Error: unknown "{self.resource_type}" resource type')
            return False

        return True

    def complete(self, *args, **kwargs):
        text, line, begidx, endidx = args[-4:]

        if self.resource_type == 'directory':
            resource_filter = lambda p: pathlib.Path(p).is_dir()
        else:
            # Directories need to be shown in file selection as well.
            resource_filter = None

        return self.menu.path_complete(text,
                                       line,
                                       begidx,
                                       endidx,
                                       path_filter=resource_filter)


class MessageCryptoWorkflow(Workflow):

    def __init__(self, menu_instance):
        super().__init__(menu_instance)

    def _clean_base64_payload(self, message: str) -> str:
        r"""Match of a Base64 string without spaces of at least 16 chars."""
        base64_pattern = r'(?:^|\s)([A-Za-z0-9+/]{16,}={0,2})(?=$|\s)'
        match = re.search(base64_pattern, message)
        if match:
            return match.group(1)
        return ''

    def start(self) -> bool:
        self.print_option_heading(
            question_prefix='What is the message you want to')

        message: str = self.menu.read_input('Input your message: ').strip()
        if not message:
            self.menu.perror('Error: Message cannot be empty. Exited.')
            return False

        if not self.encrypt:
            message = self._clean_base64_payload(message)
            if not message:
                self.menu.perror('Error: not a valid base64 payload')
                return False

        self.menu.poutput()
        password: str = self.get_password()
        if not password:
            return False

        result: dict = self.menu.scrambler.encrypt_msg(password, message,
                                                       not self.encrypt)

        self.menu._clear_terminal()
        self.menu.poutput(f'=== {self.keyword} ===')
        self.menu.poutput()

        if result['status'] == 200:
            self.menu.poutput('Operation completed.')
        else:
            self.menu.perror(result['message'])
            return False

        self.menu.poutput()
        if self.encrypt:
            self.menu.poutput(
                f'{self.menu.instance.get_crypto_suite_mappings()}: {result["output"]}'
            )
        else:
            self.menu.poutput(f'secret: {result["output"]}')

        return True
