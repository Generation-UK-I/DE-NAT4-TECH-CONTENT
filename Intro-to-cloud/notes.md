
Lambda is an **event-driven** service, it allows you to write code in a range of popular languages natively or via API call, you simply provide your code, and decide what **event** triggers it to run. You are billed for the length of time it takes to execute your function, to the second.

There are some limitations to running your functions with Lambda, your function should not:

- Exceed 15 mins (900 secs) runtime
- Consume more than 10GB of RAM, or 10GB of persistent storage
- Be more than 50MB (code and resource files) when zipped
  - If your function needs access to a lot of data, simply store it elsewhere, such as in S3

There are more, but these are the key ones to be aware of initially.




The Domain Name Service (DNS) is basically the global '*address book*' for the internet, it allows us to look up a human-friendly domain name, and receive the corresponding IP address for that target.

Just like your home needs a unique address in order to receive post, computers on the internet need a unique address in order to send and receive traffic, this address is called an IP (internet protocol) address.

This is done automatically every time you type in a web address and press enter, but you can do it manually with the NSLOOKUP (Windows) or DIG (Linux) commands





- **Cables**: Used to physically connect our devices together so they may access the network.
  - Typically copper Ethernet, but on-prem fibre-optic is becoming more common.
  - For our purposes disregard wifi, we never connect a server to the network with wifi.
- **Switches**: These devices include lots of ports into which our devices are connected via cables. So switches effectively 'form' the network.
  - The switch has lots of network ports, it receives traffic in one port, and forwards it out another
  - Almost all network traffic passes through switches.
- **Routers**: As networks become complex, we need to manage where traffic can go, and how it gets there For example the router provides a **route** to the internet.
  - The router allows you to define routes traffic can take, which allows you to permit and deny it. For example, you may want to prevent traffic from reaching an segment of your network (a **subnet**) containing resources with sensitive data.
- **Firewalls**: These devices are used to manage the traffic that is allowed access your network and resources. There are some advanced mechanisms, but at the basic level you can define ports, protocols, and IP addresses which are permitted or denyed access.
  - For example, a web server only operates on `HTTP` and/or `HTTPS`, the firewall allows you to block all traffic except this type.