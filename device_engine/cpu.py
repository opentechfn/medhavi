import base
import paramiko


class CPUEngine(base.BaseEngine):
    device = 'cpu'

    def get_properties(self, node_ip=None, username=None, password=None):
        """ Run lscpu on host machine and return the CPU information
        """
        try:
            ret = base.run_command('lscpu', node_ip, username, password)
        except Exception as e:
            raise e
        info = dict(i.strip().split(':') for i in ret)
        cpu_details = {}
        cpu_details['model_name'] = info.get('Model name').strip()
        cpu_details['architecture'] = info.get('Architecture').strip()
        cpu_details['numa_node_0'] = info.get('NUMA node0 CPU(s)').strip()
        if info.get('NUMA node1 CPU(s)'):
            cpu_details['numa_node_1'] = info.get('NUMA node1 CPU(s)').strip()
        return cpu_details
