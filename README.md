
Prerequisite:

-   Docker Desktop installed
    
-   Kubernetes enabled
    

  

Enabling Kurbernetes in Docker Desktop:

1.  Click on Settings![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXed9KSn7no3pQpe9AG7DuNZ-dBc_NkTa9g-zLgw2Aquxc2dsA6KceaMMcs7_t8ZDJyZ1nJUkTT9Xk3yrRCOoF38swvNQB-xhzPhG9RZAAxq0PCaGnbeHqh3vR_xbSMIS5KuCS7SOA?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
2.  Select Kubernetes
    

Tick Enable Kubernetes

Click Apply & Restart![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcOstpcT9PRSO5hd7PzvJpn_04z6EaRZQvldnRipbOrvYZGMkLD-7kT4x1MxyH-4U83a3jmDiRDwCK9lPMZjEjaMBQVLU-lmEnvdXzOfQNQq7-uD2Cwk5mkwnFMikPCZNwH3tJA?key=Q76yZIKrh_GMrC9c_IfTvAvZ)

3.  Select install  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe_GJFSvz8TqqSDirxlBqB0ALfK1uHaKXQ1Y_6oYITMaw6-C-9m3jwAWoLnegbrjebiHbG6UlNPcgKDzteaVwRd0I5Os3FFOUkZ8I_u138i-TLbwCuwj4rZeskGcYDkzhi55cIwEg?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    

  
  

Building Images (Email,Sql,Server,Website) :

docker-compose build

  

Master Image:

cd master

docker build -t sit-distibuted-master .

  

Slave Image:

cd slave

docker build -t sit-distributed-slave .

  

How to Run:

1.  Run in Terminal : kubectl apply -f k8s/
    
2.  kubectl get pods
    

Check that there are 4 pods running ( server, email, website, sql )

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdr5FrT9seGD1Wvu_NT4XYsEU_qzqw4vGtk4d7AELuxHvuBM1mOwUNnzJpQPX_ywTkvjOgdu28f9BSJWrZ8dZWnfwZuX_uouAxwg-6HWCA_91S2e9W9kI0lEvAwbHdmUkEFWlDjfplzrUqHKZDaDkaMbAlc?key=Q76yZIKrh_GMrC9c_IfTvAvZ)

3.  kubectl get svc
    

Check that there are 5 services running ( kubernetes, server, email, website, sql )

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXd9gI6se-c_arHjuj4pEHGT4ciAhy2xeJltlOyFLm6F7USer6WoViH429kc9NOpQ7A6oRlbjI8j8RdoMOu7ffDMlCU4r4H1T53zvMLlyIR7PUHty_BaZ9vFwkckPdOagSPXnGw8VQVFLlptyCAYobdS_Ykm?key=Q76yZIKrh_GMrC9c_IfTvAvZ)

  

4.  Access website in browser
    

1.  <ip_address>: 30001  
    Where <ip_address> is the address taken from ipconfig/ifconfig in cmd.
    

  

## Running The System

### Starting a Slave Node

To start a Slave node, we will use the following command

docker run -p 51592:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip <your-public-ip> --storage_port <your-public-port>

  

Reminder: If you want to run multiple Slave on the same device, you need to use different values for the storage_port argument.

<ip_address> is the address you get from ipconfig/ifconfig

<your-public-ip> is the ip your slave is exposing

<your-public-port> is the port your slave is exposing

### Scenario #1 - flawless system

In this scenario, we will proceed with a successful task, with no nodes being shut down

  

1.  Start a slave node using the following command:  
    docker run -p 51592:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip 192.168.1.5 --storage_port 51592![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeP2j-nGNHyrNUn0Tr5aQWchY3SKqhgbudylxsOEF8GvDwtovg5pfstz_28zyDQxun0_8NIEbayajw7x0AgM0vyZa-LBqWTPOwGHPSVN4shSfTyX9BHW1v8rmaPqbiMz8bHr9N3Kw?key=Q76yZIKrh_GMrC9c_IfTvAvZ)  
    You will notice that the this Slave node will be assigned as a Storage node  
      
    
2.  Start a second slave node using the following command:  
    docker run -p 51593:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip 192.168.1.5 --storage_port 51593  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe19jHsSz-LUaT6vtyYVnaRLopEqLytdRzy0Vwt6V25tqrG4nM4bb8qBkrnwFmd8Ed0AxAnRO0ZMTHA2MRI-Z4TZb6EI18TZWuYHeO00ZwySoUvIpZIOHgoQJ6KSpyc1koc7Hz4tA?key=Q76yZIKrh_GMrC9c_IfTvAvZ)  
    You will notice that this Slave node are also being assigned as a Storage node.  
    As a secondary storage node, it will also clone the data from the first storage node.
    
3.  Start a third slave node using the following command:  
    docker run -p 51594:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip 192.168.1.5 --storage_port 51594  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc_FsGzogf2G5sQK2-61WDYuUomO8wUrj3iTKpQo1OPjFRkmiFg0vVJ570vqWCTLVh5jkwVa80gg1rPEcQRVXK55eUrxg-HPGZttfEtI3TXfWavKM_W3-n0zdtAeJrCnSzy-eEp?key=Q76yZIKrh_GMrC9c_IfTvAvZ)  
    This time, you will notice that it is not assigned as a Slave node
    
4.  We continue to start three more slave nodes  
    docker run -p 51595:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip 192.168.1.5 --storage_port 51595  
    docker run -p 51596:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip 192.168.1.5 --storage_port 51596  
    docker run -p 51597:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip <ip_address> --port 30000 --storage_ip 192.168.1.5 --storage_port 51597
    
5.  Next, we will start a Master node with the following command:  
    docker run -p 8786:8786 -p 8787:8787 sit-distibuted-master --ip <ip_address> --port 30000  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdST1B_bteczJN5U0t6qoVQa8YonxnGcRyMC0xouPYbQbx5TMOm_kDZWSSFDijKrcKq3J68DTwnThs3AbFJFAW1TFLxSoS3ey1EFrhKl6Ey9vsrHn3LBm7J8MwftofBbVSpjugLgA?key=Q76yZIKrh_GMrC9c_IfTvAvZ)  
    You will see that the Master server is started
    
6.  As a test, on the root directory, run the send.py file. This file is supposed to be written and run by a researcher, to send a task for evaluation. To run, please edit line 13, to use the correct IP and Port number that the server is running on.  
    You may then run with this command:  
    python send.py --llm_name EleutherAI/pythia-14m  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdOauHUq_-_h_Su7A2khnSiKBPs_XLgvrU0UB4Wzj-VTfppnKeaVXR_YA7DVxLFnTc_-AGrUdRnCI34empy66BzDJwoQoXuyzHYeDhSHYiGMTDHtMqzgMqkZsZuave5468skQV2Zw?key=Q76yZIKrh_GMrC9c_IfTvAvZ)  
    You will see that the task is being sent to the server.
    
7.  Upon receiving the request from send.py, we can see on Master console that it has requested for four slaves to complete this task.  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfVi5WBuEbojiI6bVSnwmudtU-xmPFO47r2dlhM6Ojhu_3QL9UQNbntXuD4HLNqYt_hHHGsKadNGZbZS-Q_guPAUfiqFpbDWhHloBtELLUF6E175ARvELLHgRWvP8lJBNc3UqRPRQ?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
8.  On the Server console, we can also see the Master requested for four slaves, and we distribute and assign it to the Master.  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe-SiSFJaGcUja-dLWYsbW8x9olvnqO_TGHk1x7IS4oJEhH7N8b-hWU1YDl8SSeT_aOXOdoKjrG-ubbbpvCw0DJoT54ZjVJjjWGC1UownpjtrsaWlaUh9EbX9DU3YtrMNxeiD5u6g?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
9.  On the Slave consoles, we can also see that they connected to Master, received the task, and are ready to proceed with the task  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXf5R8sqp3hFKVHDWVxwoPXqc_lEHl0uTSNyygNZIpel1iPBOeHDy0bZdJDIxOlG9Cnuji3p0LPFNvVqTouBbwJiOu1IMyVXta6xi6ExZ2TbEqLzQQEM5gAIoliEFDfVEDAyPjQM?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
10.  Upon all task runs (this could take minutes), we can see from the Storage console that the result are sent to the Storage nodes  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfR1epXp9n5bp-IAUaKPh4LCrGHEoErixIWIRGHNWsetGwCxjasnlIgySqg_fWN3B_bSyTLJNZo-Qth7pm6llg9t6dyHhB804cwwyH52DzXWPbuOYlpP8Qu49_FVNk2BaHCoEBG?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
11.  Upon all results arrived, on the Master console, we can see that the result is fetched, and sent back to the researcher’s send.py.  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXduJETI09l1jhNQN4YniXI914OMVG17cwWl23rRfjiWp5dN4ktcm7QVhPO8q1vZiCoNeqsPNavXnfPSY-ykXf_YSti4QjbW0BWxNNXDROlWh6oIXCyGPsMXo0Zs3PRQJhaBOHMBfA?key=Q76yZIKrh_GMrC9c_IfTvAvZ)  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfDd3JI4rlaQUw-K71tc24FBH_d_uCVmaois6HWRF9oXciwxzCXMTDOafBmZIKJzK6bFTuUynN9C6aa0BqhBNXR9htlyLB6_f564J7-lae41vskDPKjP9y3DdHIgJgaN32C6PeEZQ?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    

### Scenario #2 - multiple failures

Now that we understand the basics, let us purposely shutdown some of the nodes, and experience the fault-tolerant of this system.

It would be good to start afresh, using the following commands:

1.  kubectl delete -f k8s/
    
2.  docker rm -v -f $(docker ps -qa)
    

  

Warning, the second command will delete all containers (even those unrelated to this project).

  

1.  Please follow [Scenario #1](https://docs.google.com/document/d/1tN9KhO8Mt05llhKZEw-_S5LlWJf3npzdye7u6s_gr5E/edit?tab=t.0#heading=h.kre6cr3xl1f1) up till step 6, where the tasks are sent out.
    
2.  Now, we will purposely shutdown one of the Slave node
    

1.  Using docker ps  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeukSl3QiLdGUxChOc6EiKrkrSQttnU4JLNkUSloDu_tBDOjOLMHHOxTsieTVmOKzfr0FarMRH-W1S5MyNZhnvgT5uXB39UbNGEWi3vD8I4GJMzkA0Y9lfGInJkmnX2vAUnHQH0?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
2.  We will shutdown the 51585 slave node with docker stop a1e8003cec7b  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXc6YiM3syrEhDG8TlRDW85U2QXhCU1BDDtU_YO0-M4q1ytGwyprWAjB8wzOWjeTY6KRJelqcr6Y0psJpBT4n8px0eubRJNGZ6LFLHxho_HTVCJV_vHashsDz7mL9YPupqcTI2yKog?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
3.  Here, we can see that despite one of the slave nodes being down, there is still one other slave node doing the same task. Hence, there is task duplication for fault tolerant.
    

4.  Now, we will purposely shut down our Master node with the command:  
    docker stop 030357dfca61  
    Upon stopping, we can see in the console of send.py that the Master node is down. And it will keep retrying to reconnect.  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXe8coW5pa6KxzRbts6XiYgDS6QzrMw6KS9joaPTlotxZxytXTNQ6Hr5Oft0A1Qk0gxMs3bk_0XKCRFDsAQr8TltxupymJFn96quzjzc8k95ay5u0CQEb6VMaKFU0mLtLV-2fQ7T4A?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
5.  Now, we can start the Master node again. Here, we see that send.py sends the same request. However, our Master is smart enough to know that this request is being processed. Thus, there is no need to request for four move slaves (saving resources of the computation pool).  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdRq7Xg-B4EpW56qUY4zUwbP0dXBOamI1tyC0Uai2iCVE5Bctmal-rIe-sfm51kbYD8H5lzaw2MKWRXYk2J7u-y8zYTkeV2zYYzhlhF7kb5ne9qlNTg9Z0DwloWBryE5h8C1dSO?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
6.  Now, when there is only one result sent to the storage node, we shall purposely shutdown one of the storage nodes using the same docker stop command.
    
7.  On the Server console, we can see that it detected that the storage node is down  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdPEWsL7lUzxigd-Wjy0i7kaDWtRrOuOXG_-rzaDK2loaf5NLTV2a5BhOCtOloKYFtds4R-wdNHY1HjRF6skQHtdpdDvheOHk7YvH5L4tYpLr1pIHtcdPe4d8hxASTUI9vfzaPV?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
8.  When the tinyMMLU task finishes, the slave node automatically reconnects back to the server. The server would recognize that one of the Storage nodes is down, and then promote this newly connected Slave node to become a Storage node.  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdUvoNx0RnN3vvIgPiCqvbgcnn04cxmv8rOV3Hh06Tr6RCwL7h9Obab3O5PcKouOL-d7gZnWENRP-0_DfTSzhhx0bQpHSvlw_t3sCbflx_4Gt6XT99jowXcduYto2vpadu_zgvk?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
    
9.  Despite all these nodes being down, in the end, our send.py would still receive the result back. Thanks to the fault tolerance measures that our system has provided.  
    ![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXclDc54XuTppOaUMmuNlHozt2BpTi-roa4D8PJBq8ISihqgsrYdRhzEIAqM6M7J2zG5rw_Zf_1dlo1KIdoNX9_3QUaDqTr50u6iM7O4gwiKyscMrkO4oYs_Jk7DQ2QzfMwOrhtSnA?key=Q76yZIKrh_GMrC9c_IfTvAvZ)
