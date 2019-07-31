medhavi
Intelligent Infrastructure
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
