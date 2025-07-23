- [c++ - What is SOCK_DGRAM and SOCK_STREAM? - Stack Overflow](https://stackoverflow.com/questions/5815675/what-is-sock-dgram-and-sock-stream )
    - TCP almost always uses `SOCK_STREAM` and UDP uses `SOCK_DGRAM`.
    - TCP (`SOCK_STREAM`) is a connection-based protocol. The connection is established and the two parties have a conversation until the connection is terminated by one of the parties or by a network error.
    - UDP (`SOCK_DGRAM`) is a datagram-based protocol. You send one datagram and get one reply and then the connection terminates.
        - If you send multiple packets, TCP promises to deliver them in order. UDP does not, so the receiver needs to check them, if the order matters.
        - If a TCP packet is lost, the sender can tell. Not so for UDP.
        - UDP datagrams are limited in size, from memory I think it is 512 bytes. TCP can send much bigger lumps than that.
        - TCP is a bit more robust and makes more checks. UDP is a shade lighter weight (less computer and network stress).
    - Choose the protocol appropriate for how you want to interact with the other computer.

- 本机序 & 网络序 [c - Understanding htonl() and ntohl() - Stack Overflow](https://stackoverflow.com/questions/36924598/understanding-htonl-and-ntohl )
    - As others have mentioned, both `htons` and `ntohs` reverse the byte order on a little-endian machine, and are no-ops on big-endian machines.
    - What wasn't mentioned is that these functions take a 16-bit value and return a 16-bit value. If you want to convert 32-bit values, you want to use `htonl` and `ntohl` instead.
    - The names of these functions come from the traditional sizes of certain datatypes. The `s` stands for `short` while the `l` stands for `long`. A `short` is typically 16-bit while on older systems `long` was 32-bit.
    - In your code, you don't need to call `htonl` on `rec_addr`, because that value was returned by `inet_addr`, and that function returns the address in network byte order.
    - You do however need to call `htons` on `rec_port`.

- [c - How to convert a string to a number? - Stack Overflow](https://stackoverflow.com/questions/171223/how-to-convert-a-string-to-a-number )
    - `atoi` is a function that converts a string to an integer.
    - `strtol` is a function that converts a string to a long integer.
    - `strtod` is a function that converts a string to a double.
    - `strtoul` is a function that converts a string to an unsigned long integer.
    - `strtoll` is a function that converts a string to an unsigned long long integer.
    - `strtoull` is a function that converts a string to an unsigned long long integer.
    - `strtod` is a function that converts a string to a double.
    - `strtof` is a function that converts a string to a float.
    - `strtold` is a function that converts a string to a long double.

- htons() & ntohs() [c - How to convert a string to a number? - Stack Overflow](https://stackoverflow.com/questions/171223/how-to-convert-a-string-to-a-number )
    - `htons` is a function that converts a 16-bit value to a network byte order value.
    - `ntohs` is a function that converts a network byte order value to a 16-bit value.

