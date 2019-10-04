import paramiko
from conf import ssh_conf as conf_file
import socket


class SSH_Util:

    def __init__(self):
        self.host = conf_file.HOST
        self.username = conf_file.USERNAME
        self.password = conf_file.PASSWORD
        self.commands = conf_file.COMMANDS
        self.pkey = conf_file.PKEY
        self.port = conf_file.PORT
        self.timeout = float(conf_file.TIMEOUT)

    def connect(self):
        try:
            print("Establishing ssh connection")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # connection to the server

            if(self.password == ''):
                print("Hi", self.pkey)
                self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    pkey=self.pkey,
                    timeout=self.timeout,
                    allow_agent=False,
                    look_for_keys=False,
                    )
                print ('Connected to the server', self.host)
            else:
                self.client.connect(
                    hostname=self.host,
                    username=self.username,
                    password=self.password,
                    timeout=10,
                    allow_agent=False,
                    look_for_keys=False,
                    )
                print ('Connected to the server', self.host)
        except paramiko.AuthenticationException, \
            authenticationException:
            print 'Authentication failed, please verify your credentials'
            result_flag = False
        except paramiko.SSHException, sshException:
            print 'Could not establish SSH connection: %s' \
                % sshException
            result_flag = False
        except socket.timeout, e:
            print 'Connection timed out'
            result_flag = False
        except Exception, e:
            print '\nException in connecting to the server'
            print ('PYTHON SAYS:', e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        return result_flag
    def execute_command(self,commands):
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                for command in commands:
                    print "Executing command --> {}".format(command)
                    stdin, stdout, stderr = self.client.exec_command(command,timeout=10)
                    self.ssh_output = stdout.read()
                    self.ssh_error = stderr.read()
                    if self.ssh_error:
                        print "Problem occurred while running command:"+ command + " The error is " + self.ssh_error
                        result_flag = False
                    else:    
                        print "Command execution completed successfully",command
                    self.client.close()
            else:
                print "Could not establish SSH connection"
                result_flag = False   
        except socket.timeout as e:
            print "Command timed out.", command
            self.client.close()
            result_flag = False                
        except paramiko.SSHException:
            print "Failed to execute the command!",command
            self.client.close()
            result_flag = False    
 
        return result_flag

if __name__ == '__main__':
    print 'Start of %s' % __file__
    ssh_obj = SSH_Util()
    if ssh_obj.execute_command(ssh_obj.commands) is True:
        print("Commands executed successfully\n")
    else:
        print("Unable to execute the commands")
 
