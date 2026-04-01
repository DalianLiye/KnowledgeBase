# VPC
VPC 是 AWS 云中创建一个逻辑隔离的虚拟网络环境

## VPC Attribute

- Details tab	
  - VPC ID	
    VPC的ID， 格式为vpc-XXXX
  - State	
    VPC当前状态， Available
  - Block Public Access	
    是否启用防止VPC中的资源（如子网、实例、存储等）被意外或故意暴露到公共互联网功能\
    On：防止公网访问呢\
    Off：允许公网访问\
  - DNS hostnames	
    是否启用为VPC中的实例自动分配基于DNS的主机名功能（Enable | Disable）\
    当启用时，如果VPC中启动新实例(如EC2实例)，该实例会自动获得一个私有DNS主机名，格式：ip-XX-XX-XX-XX.ec2.internal，这个私有DNS主机名可以用于实例之间的名称解析，方便内部通信，而不必直接使用IP地址\
    该属性通常和DNS resolution属性 （是否启用 DNS 解析）一起使用\
    DNS hostnames负责拿到新主机名，DNS resolution负责解析拿到的主机名
  - DNS resolution	
    是否启用DNS解析功能，即VPC内的实例可以使用VPC提供的DNS服务器（通常是云厂商的内部DNS服务）来将域名解析成IP地址 （Enable | Disable）
  - Tenancy	
    VPC中启动的EC2实例的租用类型\
    Default（默认）\
    Dedicated（专用）\
    Host（专用主机）\
    VPC中启动的EC2实例的租用类型，不同的租用类型对应不同的作用，成本也不一样，比如：\
    Default（默认）: EC2实例运行在共享的物理服务器上，共享硬件, 适用于大多数普通应用，成本较低\
    Dedicated（专用）: EC2实例运行在专用的物理服务器上，不共享硬件 适用于需要物理隔离的安全合规场景\
    Host（专用主机）: EC2实例运行在整台物理服务器，自主控制这台物理服务器上创建多少实例，适用于高度控制硬件环境，满足特定合规需求
  - DHCP option set	
    VPC关联的DHCP option set（DHCP选项集）
  - Main route table	
    默认route table ID\
    创建VPC时会自动生成一个route table，这个自动生成的route table就是默认的route table，也叫main route table\
    如果subnet没有显式关联其他route table，就会默认使用这个main route table
  - Main network ACL	
    默认network ACL ID\
    创建VPC时会自动生成一个network ACL，这个自动生成的network ACL就是默认的 network ACL，也叫main network ACL\
    如果subnet没有显式关联其他network ACL，就会默认使用这个main network ACL
  - Default VPC	
    是否为默认的VPC（Yes | No）\
    创建账号时，会自动创建一个默认的VPC，便于快速上手，开箱即用
  - IPv4 CIDR	
    VPC的IPv4 IP地址段，比如\
    10.77.204.0/24\
    100.64.0.0/20
  - IPv6 CIDR	
    VPC的IPv6 IP地址段
  - Network Address Usage metrics	
    是否启用监控和展示VPC内IP地址资源使用情况的统计数据和指标的功能（Enable | Disable）
  - Route 53 Resolver DNS Firewall rule groups	
    VPC关联的Network firewall rule group\
    Route 53 Resolver DNS Firewall rule groups 主要是通过定义一组规则（rule groups），对VPC内发出的DNS请求进行过滤和控制，从而防止恶意或不合规的DNS解析请求，保护网络安全\
  - Owner ID	
    VPC的实际拥有者（创建者），AWS account id
- Resource Map Tab		
  VPC内的各种资源及其相互关系
- Flow logs Tab	
  捕获和记录进出VPC子网或网络接口的IP流量信息
- Tags Tab	
  VPC的标签


# Subnet
subnet是VPC内的空间划分，将VPC分成更小的网络段，是VPC下的子网

# Subnet Attribute
- Details tab
  - Subnet ID
    Subnet的ID
  - Subnet ARN
    Subnet ARN
  - State	
    Subnet当前状态,Available
  - Block Public Access	
    是否启用防止subnet中的资源（如子网、实例、存储等）被意外或故意暴露到公共互联网功能\
    On：防止公网访问呢\
    Off：允许公网访问\
    1) VPC的Block Public Access是全局开关，Subnet的Block Public Access是局部开关，用于更细粒度的控制
    2) VPC和subnet的Block Public Access的值可以不一致，逻辑如下：
    VPC	Subnet	Comment\
    On	On	子网无法关闭，强制阻止公共访问\
    Off	On/Off	子网可单独开启或关闭公共访问阻止策略
  - IPv4 CIDR	
    Subnet的IPv4 IP地址段，比如\
    10.77.204.0/24\
    100.64.0.0/20\
  - Available IPv4 addresses	
    Subnet内可用的IPv4地址的数量
  - IPv6 CIDR	
    Subnet的IPv6 IP地址段
  - IPv6 CIDR association ID	
    Subnet和VPC分配给subnet的IPv6 CIDR的关联关系ID
  - Availability Zone	\
    Subnet所在的可用区\
    一个Subnet必须要指定一个可用区\
    一个Subnet只能指定一个可用区\
    一个可用区可以指定多个Subnet
  - VPC	
    Subnet所在的VPC, 格式：<VPC ID> | <VPC name>
  - Route table	
    Subnet关联的route table\
    每个Subnet必须关联一个route table
  - Network ACL	
    Subnet关联的Network ACL
  - Default subnet	
    是否为默认subnet (Yes | No)\
    创建VPC时，会为每个可用区自动创建Subnet，这个Subnet就是Default Subnet
  - Auto-assign public IPv4 address	
    是否为subnet中创建的实例自动分配公网IPv4地址 (Yes | No)\
    如果不是自动分配，那么只能手动分配
  - Auto-assign IPv6 address	
    是否为subnet中创建的实例自动分配IPv6地址  (Yes | No)\
    如果不是自动分配，那么只能手动分配
  - IPv4 CIDR reservations	
    保留的IPv4地址\
    保留一些IPv4地址，确保这些地址不会被自动分配给实例或其他资源
  - IPv6 CIDR reservations	
    保留的IPv6地址\
    AWS用来管理和保留子网中部分 IPv6 地址范围的机制，确保这些地址不会被自动分配给实例或其他资源
  - IPv6-only	
    是否只支持IPv6(Yes | No)
  - Hostname type	
    分配给subnet内设备的主机名（Hostname）的类型或格式(IP name)
  - Resource name DNS A record	
    是否启用将一个主机名（资源名称）映射到一个IPv4地址的功能 (Enable|Disabled)
  - Resource name DNS AAAA record	
    是否启用将一个主机名（资源名称）映射到一个IPv6地址的功能 (Enable | Disabled)
  - DNS64	
    是否启用DNS64功能 (Enable | Disabled)\
    DNS64是一种 DNS 服务器功能，能够将 IPv4 地址转换成对应的 IPv6 地址，从而让 IPv6-only 主机能够通过IPv6地址访问 IPv4-only 服务器
  - Owner ID	
    Subnet的实际拥有者（创建者）, AWS account id
- Flow logs Tab		
  捕获和记录进出Subnet子网或网络接口的IP流量信息
- Route table Tab	
  - Destination	
    与当前subnet关联的route table中，流量数据包的目标地址范围(下一跳)
  - Target	
    与当前subnet关联的route table中，流量匹配到Destination后，数据包被转发地址\
    local：本地子网或本地设备
- Network ACL Tab	
  - Inbound rules	
    入栈规则
  - Outbound rules	
    出栈规则
- CIDR reservations Tab		
  保留的CIDR地址
- Sharing Tab		
  subnet里的资源是否以及如何被多个用户、项目或账户共享使用
- Tags Tab		
  subnet的标签

# Route tables
决定数据包该往哪里走。每个子网都关联一个路由表

## Route tables Attribute
- Details Tab	
  - Route table ID	
    Route table 的ID	
  - Main
    是否是默认Route table(Yes|No)\
    创建VPC时会自动生成一个route table，这个自动生成的route table就是main route table\
    如果subnet没有显式关联其他route table，就会默认使用这个main route table
  - Explicit subnet associations
    关联该route table的subnet, 格式：<subnet id> / <subnet name>
  - Edge associations
    关联该route table的某些边缘网络资源（如边缘路由器、边缘网关、Transit Gateway、VPN网关、Direct Connect Gateway等）\
    Edge Associations 在路由表中主要用于管理和控制流量如何通过边缘设备或边缘网络节点进行转发
  - VPC
    Route Table所在的VPC, 格式：<VPC ID> | <VPC name>
  - Owner ID
    route table的实际拥有者（创建者）,AWS account id
- Routes Tab/Routes
  - Destination	
    流量数据包的目标地址范围
  - Target	
    流量匹配到Destination后，数据包被转发地址(下一跳)\
    local：本地子网或本地设备\
    nat网关 id
  - Status	
    当前route 记录的状态, Available
  - Propagated
    是否是传播路由(Yes|No)\
    Propagated（传播路由）是指通过动态路由协议自动添加到route table中的路由条目，通常来自于VPN连接、Direct Connect（专线连接）或虚拟私有网关（Virtual Private Gateway）等

- Subnet associations Tab
  - Explicit subnet associations
    明确指定使用当前route table的subnet
  - Subnets without explicit associations	
    没有明确指定使用任何route table的subnet
- Edge associations Tab		
  Edge associations明细
- Route Propagation		
  Route Propagation明细
- Tags Tab		
  Route table的标签


# Internet gateways
让VPC内的资源能访问互联网


# Egress only internet gateways
专门为IPv6设计的"单向门"，只允许从VPC内部访问互联网，但不允许互联网主动访问VPC内部


# DHCP option sets
网络配置的"说明书"，自动分配IP地址和DNS设置\
比如新的EC2启动的时候，就会自动分配配置，配置在VPC上


## DHCP option sets Attribute

- DHCP option sets
  - Options\
    DHCP服务器向VPC内的实例分配的网络配置信息\
    Options 是一组键值对（key-value pairs），用于指定DHCP服务器向VPC内的实例分配的网络配置信息

- Details Tab
  - DHCP option set ID\
    DHCP option set的ID
  - Domain name	\
    实例启动时通过DHCP自动获取的域名后缀（Domain Name Suffix）
  - Domain name servers	
    实例启动时通过DHCP自动获取的 DNS服务器 的IP地址
  - NTP servers	
    NTP服务器的IP地址
  - NetBIOS name servers
    指定的是用于NetBIOS名称解析的服务器地址
    NetBIOS（Network Basic Input/Output System）是一种用于局域网中计算机名称解析和通信的协议，主要用于Windows网络环境。
    NetBIOS name server（也称为 WINS 服务器，Windows Internet Name Service）负责将NetBIOS计算机名解析为IP地址，类似于DNS解析域名
  - NetBIOS node type	
    实例（主要是Windows实例）如何通过NetBIOS协议解析计算机名称的方式
  - Owner
    DHCP option sets 的实际拥有者（创建者）,(AWS account id)
  - IPv6 preferred lease time (seconds)	
    通过 DHCPv6 协议分配给客户端的 IPv6 地址的“首选租约时间”
    1) 租约时间（Lease Time）：指客户端（比如EC2实例）从DHCP服务器获得的IP地址的有效时间
    2) 首选租约时间（Preferred Lease Time）：这是IPv6地址的首选状态持续时间，表示客户端可以正常使用该IPv6地址的时间长度
    3) 作用是控制IPv6地址的生命周期，影响客户端何时需要更新或重新请求IPv6地址
- Tags Tab		
  DHCP option sets的标签


# Elastic IPs
Elastic IPs（弹性IP地址） 是一种静态的、可公开访问的IPv4地址，主要用于将云资源（如EC2实例）绑定到一个固定的公网IP上


# Managed prefix lists
一种方便管理和复用一组CIDR地址块的资源


# Endpoints
Endpoints（端点） 是一种网络资源，允许在不经过公网的情况下，私密地连接到AWS服务或私有服务


## Endpoints Attribute
- Endpoints	
  - Network interfaces	
    创建的弹性网络接口(ENI，Elastic Network Interface)	
  - Subnets	
    弹性网络接口（ENI）所在的subnet
  - Endpoint ID	
    Endpoint的ID
  - Status
    当前endpoint的状态 (Available)
  - Creation time	
    Endpoint创建时间
  - Endpoint type
    Endpoint类型(Gateway)
  - VPC ID	
    Endpoint所在的VPC
  - Status message	
    Endpoint当前状态的详细信息或原因的文本说明
  - Service name	
    Endpoint的service name
  - Private DNS names enabled
    是否启用私有DNS名称 (Yes|No)
- Route tables Tab	
  Endpoint的route table	
- Policy Tab	
  Endpoint的policy	
- Tags Tab	
  Endpoint的标签


# Endpoint service
让其他人能访问您VPC内服务的"接口"


# NAT gateways
让私有子网的资源能单向访问互联网（只能出去，外面进不来）


## NAT gateways Attribute

- Details Tab	
  - NAT gateway ID	
    NAT gateway的ID	
  - Connectivity type	
    NAT gateway与外部网络（通常是互联网）连接的方式或类型,(Private)
  - State
    当前NAT gateway的状态(Available)
  - State message	
    NAT Gateway当前状态的详细信息或状态说明
  - NAT gateway ARN	
    NAT gateway的ARN
  - Primary public IPv4 address	
    NAT gateway的主要公网IPv4地址
  - Primary private IPv4 address	
    NAT gateway的主要私网IPv4地址
  - Primary network interface ID	
    NAT gateway关联的network interface
  - VPC	
    NAT gateway所在的VPC
  - Subnet	
    NAT gateway所在的subnet
  - Created	
    NAT gateway的创建时间
  - Deleted
    NAT Gateway是否已经被删除或处于删除状态
- Secondary IPv4 address Tab	
  NAT Gateway的附加公网IPv4地址信息
- Monitoring Tab	
  NAT Gateway的监控信息	
- Tags Tab	
  NAT Gateway的标签


# Peering connections
VPC建的对等连接，多个VPC之间建立互通


# Network ACLs
在子网层面控制流量，绑定到子网上，是针对于子网的安全组


## Network ACL Attribute

- Network ACLs
  - Name	
    Network ACL的Name
  - Network ACL ID	
    Network ACL的ID
  - Associated with	
    与Network ACL关联的subnet列表
  - Default	
    是否是默认的Network ACL
  - VPC ID	
    Network ACL所在的VPC ID
  - Inbound rules count	
    Network ACL 入栈规则数量
  - Outbound rules count	
    Network ACL 出栈规则数量
  - Owner
    Network ACL的实际拥有者（创建者）,AWS account id
- Subnet Associations Tab
  关联的Network ACL
- Tags tab
  Network ACL的标签


# Security Groups
是一种虚拟防火墙，用于控制进出云资源（如虚拟机实例、数据库等）的网络流量

# Security Groups Attribute
Layout	Attribute	Description

- Security Groups
  - Security group ID	
    Security Group的ID
  - Security group name	
    Security Group的Name
  - VPC ID	
    Security Group所在的VPC ID
  - Description	
    Security Group的description
  - Owner
    Security Group 的实际拥有者（创建者）AWS account id
  - Inbound rules count	
    Security Group 入栈规则数量
  - Outbound rules count	
    Security Group 出栈规则数量
- Sharing - new tab	
  当前security group共享给其他账号的详细信息
- VPC associations - new Tab	
  当前security group与不同VPC关联的详细信息
- Tags	
  Security Group的标签


# Transit gateways
Transit gateway用于充当多个VPC、VPN连接和本地网络之间的枢纽，达到简化和集中管理的目的

## Transit gateways Attribute

- Transit gateways
  - Name	
    Transit gateway的Name
  - Transit gateway ID	
    Transit gateway的ID
  - State
    当前Transit gateway的状态(Available)
  - Amazon ASN
    ASN(Autonomous System Number)
	自治系统编号，用于唯一标识一个自治系统（AS）
  - DNS support
    是否启用跨VPC的DNS解析功能的设置(Enable|Disabled)
  - VPN ECMP support
    是否支持通过多个VPN连接实现等价多路径路由的功能(Enable | Disabled)
  - Auto accept shared attachments
    是否自动接收处理来自其他AWS账户或组织单位（OU）共享的附件（attachments） (Enable | Disabled)
  - Default association route table
    新创建的Transit Gateway附件（比如VPC、VPN连接等）是否关联到默认route table
    Enable：启用默认关联路由表功能，新创建的附件会自动关联到指定的默认route table ID
    Disabled：禁用默认关联路由表功能，新附件不会自动关联任何route table，需要手动关联
  - Multicast support
    是否支持多播流量的转发和管理功能(Enable | Disabled)
  - Security Group Referencing support
    是否支持安全组（Security Group）规则中直接引用其他VPC中的安全组(Enable | Disabled)
  - Association route table ID	
    关联的route table ID
  - Default propagation route table	
    默认传播路由表
    Enable ：所有新连接的附件会自动将它们的路由传播到这个默认的路由表
    Disabled：所有新连接的附件会不会自动将它们的路由传播到这个默认的路由表
  - Propagation route table ID	
    具体的传播路由表信息
  - Transit gateway CIDR blocks	
    为Transit Gateway分配的一组私有IP地址范围
- Details Tab	
  - Transit gateway ARN	
    Transit gateway的ARN，可以是跨账号
- Flow logs Tab	
  捕获和记录进出VPC子网或网络接口的IP流量信息
- Sharing Tab		
- Tags Tab		
  Transit gateway的标签


## Transit gateway attachments
Transit Gateway Attachments（附件）是指连接到Transit Gateway的各种网络资源或连接，它们通过附件与Transit Gateway建立通信路径，实现网络互联

- Transit gateway attachments
  - Name
    Transit gateway attachments的Name
  - Transit gateway attachment ID
    Transit gateway attachments的ID
  - Transit gateway ID
    关联的Transit gateway的ID
  - State
    当前状态（available）
  - Resource type
    Transit gateway attachments的资源类型
  - Resource ID	
    资源ID
  - Association route table ID	
    关联的route table ID
  - Association state	
    关联的状态（Associated）

- Details Tab
  - Resource owner ID		
    Transit gateway attachment的实际拥有者（创建者）（AWS account id）
  - IPv6 support	
    是否支持IPv6
  - Transit gateway owner ID	
    关联的Transit gateway 的owner ID
  - DNS support	
    是否启用跨VPC的DNS解析功能的设置(Enable|Disabled)
  - Security Group Referencing support	
    是否支持安全组（Security Group）规则中直接引用其他VPC中的安全组(Enable|Disabled)
  - Appliance Mode support
    是否启用支持Appliance模式 (Enable|Disabled)
  - Subnet IDs	
    Transit gateway attachment（尤其是VPC附件）关联的subnet ID列表
- Flow logs Tab
  捕获和记录进出VPC子网或网络接口的IP流量信息
- Tags Tab
  Transit gateway的标签


# Traffic Mirroring
Traffic Mirroring（流量镜像） 用于复制VPC中指定网络接口（ENI）的入站和出站流量，并将这些复制的流量发送到指定的目标（如监控或安全设备）进行分析