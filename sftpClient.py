import paramiko 

class SFTPClient:
    def __init__(self, server, key_filename=None, username=None, password=None):
        self.ssh = self.__open_ssh(server, key_filename, username, password)
        self.sftp = self.ssh.open_sftp()

    def __open_ssh(self, server, key_filename, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
            ssh.connect(server, key_filename=key_filename, username=username, password=password)
            return ssh
        except Exception as e:
            raise SFTPConnectionError(f"Failed to establish SSH connection: {e}")


    def open(self, remotepath, mode='wb'):
        try:
            return self.sftp.open(remotepath, mode)
        except Exception as e:
            raise SFTPError(f"Failed to open remote file: {e}")

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()

class SFTPConnectionError(Exception):
    pass

class SFTPError(Exception):
    pass