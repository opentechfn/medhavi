import abc
import six

@six.add_metaclass(abc.ABCMeta)
class BaseEngine(object):

    device = None

    @abc.abstractmethod
    def get_properties(self):
        """Return the device information
        """

def run_command(cmd):
    # Replace this code by the SSH module
    import paramiko
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='localhost',
                       username='ubuntu', password='ubuntu')
    stdin, stdout, stderr =ssh_client.exec_command(cmd)
    return stdout.readlines()

         

