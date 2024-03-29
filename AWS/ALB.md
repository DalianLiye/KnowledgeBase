AWS Application Load Balancer (ALB) 是一种托管式负载均衡器，用于在 AWS 中分配传入的网络流量到多个后端目标\
它是一项高度可靠且高性能的服务，可以帮助用户实现应用程序的高可用性和可扩展性

AWS ALB 主要用于以下方面

- 负载均衡：ALB 可以根据用户定义的规则和策略将传入的流量分发到多个后端目标（例如 Amazon EC2 实例、容器、IP 地址等）上，以提高应用程序的可用性和吞吐量

- 动态请求路由：ALB 支持基于请求的路由，可以根据请求的内容和源信息将流量分发到不同的目标组。这使得用户可以根据特定的业务需求将请求发送到适当的目标

- 固定负载均衡：ALB 支持将请求粘性地绑定到特定的后端目标，以确保来自同一客户端的请求始终转发到同一目标。这对于需要保持会话状态的应用程序非常有用

- 安全性：ALB 支持与 AWS Certificate Manager (ACM) 集成，可以轻松地为应用程序配置 SSL/TLS 加密。此外，ALB 还可以通过 AWS WAF (Web Application Firewall) 来保护应用程序免受常见的网络攻击

- 监测和日志记录：ALB 可以生成详细的访问日志和监控指标，以帮助用户实时监控应用程序的性能和流量分发情况。这些日志和指标可以与 AWS CloudWatch 集成，从而支持自动化报警和事件响应
