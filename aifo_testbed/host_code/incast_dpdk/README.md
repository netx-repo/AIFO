# server

Compile:
`make`

Run:
`sudo ./build/server rver --lcores 0@0,1@1,2@2,3@3,4@4,5@5,6@6,7@7`

### Note:
- `-l` denotes the list of thread IDs.


# client

Compile:
`make`

Run:
`sudo ./build/client --lcores 0@0,1@1,2@2,3@3,4@4,5@5,6@6,7@7 -- -n2 -r12 -s3000 -p9000 -T50`
### Note:
- `-l` denotes the list of thread IDs.
- `-n2`: specify the client_ip (id): "10.1.0.<2>"
- `-r12`: specify the receiver ip (id): "10.1.0.<12>"
- `-s3000`: maximum sending rate
- `-p9000`: Destination port
- `-T50`: Time to run

