Medhavi - Intelligent Infrastructure

Madhavi offers the “Intelligence mapping services” to translate the workload
intent to traits available in Open Infrastructure. This service my meet the
75-80% of guarantees under given constraints. The idea here is to use
infrastructure effectively without resorting to costly tuning and manual
optimization.

What is Infrastructure: Infrastructure is any kind of resource like Baremetal,
Virtual Machines, Containers or any other instance of a device or clusters on
which one executes applications or functions. Infrastructure can be described
as Templates with traits associated with its attributes.

What is Intelligence? Intelligence herein is the qualitative intent, expressed
as hints or traits that can be used to place and Manage the expectations of the
type of workload with the real-time constraints.
Real-time constraints will be specified like execution time (hr, min, sec),
precision (FP64, FP32, Int16, In8), latency ( < 1ms, between 1-10 ms,
20 ms, >100ms). This can be managed by policy profiles.

Profiles - Policies Profile per workload type will help Medhavi Intelligence
Service to use hints and traits to deliver meeting the real-time constraints
on Infrastructure.

To start one would restrict to Policy profiles providing rules to optimize the
defined KPIs to 80%. Once that is achieved one can use the AB testing idea to
distibute 20% of the load to a different workload type cluster or node to
observe how KPIs can be improved to achiever say 90% optimization.
Thus this will give possible potential to collect data on workload and profiles
that can be learned over a period to achieve better resource utilization etc.

Medhavi Design:

We will start with Medhavi Compute Workload Manager to enable the Medhavi API through A primary and secondary controllers. The API certainly will start with Baseline API support to run job in a container, VM or a Baremetal object. At this time we will not dwell into task level, and assume Job level scheduling should suffice.

The other assumption we make is that since all workloads these day assume a cluster we will assume our standard cluster to be made of 4 nodes(1-4) with agents and node(0) as agent manager. Node may be Containers, VMs or Physical servres and for PoC they will be host endpoints. We alos assume for now that we have a DB Manager with Primary Controller managing DB schemas for persistance, and some message to publish & subscribe resources and nodes for cluster to carry put job operations.

Following is the elements of Medhavi to manage the workload Intelligently.

Baseline APIs(Medhavi): Note each job must get a minimum of 1 virtual core to execute and all jobs run in parallel
ConfigNode: Config Node Agt
MonNode: Monitor Node
RunJ: init job
CancelJ: terminate job
InfoS: get status of system
InfoQ:status of Job(s)
InfoJ: Job state (steps completed or remaining)
InfoJ: Timit (start, elapsed, limit)
InfoMap: Map of nodes running job
InfoTopo: Topology view of Map
DB.ValidUsers
DB.ValidClusters
DB.ValidAccounts

https://go.gliffy.com/go/share/image/sys6fe15wgf6jre8ibm3.png?utm_medium=live-embed&utm_source=custom
