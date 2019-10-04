import base
import paramiko

class CPUEngine(base.BaseEngine):
    device = 'cpu'

    def get_properties(self):
        """ Run lscpu on host machine and return the CPU information
        """
        try:
            ret = base.run_command('lscpu')
        except Exception as e:
            raise e
        info = dict(i.strip().split(':') for i in ret)
        return info

