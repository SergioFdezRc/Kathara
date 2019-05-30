import netkit_commons as nc
import utils as u
from kubernetes import config

import link_deployer
import machine_deployer


def deploy(machines, links, options, path, no_machines_tmp=False, network_counter=0):
    # Loads the configuration of the master if it's not print mode
    if not nc.PRINT:
        config.load_incluster_config()

    namespace = "default"

    # TODO: This be used later...
    print "Namespace is %s" % str(u.generate_urlsafe_hash(path))
    # namespace = str(u.generate_urlsafe_hash(path))
    # KubernetesDeployer.get_instance().create_namespace(lab.name)

    print "Deploying networks..."
    netkit_to_k8s_links = link_deployer.deploy_links(
                            links,
                            namespace=namespace,
                            network_counter=network_counter
                          )

    # Writes the network list in the temp file
    if not nc.PRINT:
        u.write_temp(" ".join(netkit_to_k8s_links.values()), namespace + '_links', nc.PLATFORM, file_mode="w+")

    print "Deploying machines..."
    k8s_machines = machine_deployer.deploy(
                        machines,
                        options,
                        netkit_to_k8s_links,
                        path,
                        namespace=namespace
                   )

    # Writes the machines list in the temp file (only if no_machines_tmp is False)
    if not no_machines_tmp:
        if not nc.PRINT:
            u.write_temp(" ".join(k8s_machines.values()), namespace + '_machines', nc.PLATFORM)
