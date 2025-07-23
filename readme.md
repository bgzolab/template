
- front-end
  - tokenizer
  - parser
  - code generator
- back-end
  - virtual machine
  - B-tree
  - pager
  - os interface

## P01

- **REPL** (read-execute-print loop)
  - 读取﹣求值﹣输出循环 / **交互式顶层构件**
  - 一个编程环境. 因它能立刻对初学者做出回应. 对学习一门语言具有很大的帮助.
  - via: [wikipedia](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop).
- ✖ B Tree
  - via: [Youtube-29:45](https://www.youtube.com/watch?v=aZjYr87r1b8).
- `size_t` & `ssize_t`
  - `size_t `
    - 32 Bit: `typedef unsigned int size_t;`.
    - 64 Bit: `typedef unsigned long size_t;`.
    - 注意写函数的时候, 无符号数不要和符号数比较.
      ```c
      #include <stdio.h>
      #include <string.h>
      int main(){
          int i = -1;
          if(i > strlen("Demon")) printf("Hello World");
          else printf("Hello Demon");
          return 0;
      } //Hello World via http://demon.tw/programming/c-size_t-pitfall.html
      ```
  - `ssize_t `
    - 32 Bit: `int`.
    - 64 Bit: `long int`.
    - via: https://blog.csdn.net/bzhxuexi/article/details/19899803 & https://stackoverflow.com/questions/2550774/what-is-size-t-in-c
- getline in C.
  - ```c
    // from https://c-for-dummies.com/blog/?p=1112
    #include <stdio.h>
    
    int input(char *s,int length);
    
    int main(){
        char *buffer;
        size_t bufsize = 32;
        size_t characters;
    
        buffer = (char *)malloc(bufsize * sizeof(char));
        if( buffer == NULL){
            perror("Unable to allocate buffer");
            exit(1);
        }
    
        printf("Type something: ");
        characters = getline(&buffer,&bufsize,stdin);
        printf("%zu characters were read.\n",characters);
        printf("You typed: '%s'\n",buffer);
    
        return(0);
    }
    // case two
    #include <stdio.h>
    
    int input(char *s,int length);
    
    int main()
    {    
        char *b;
        size_t bufsize = 0;
        size_t characters;
    
        printf("Type something: ");
        characters = getline(&b, &bufsize, stdin);
        printf("%ld\n", bufsize);
        printf("%zu characters were read.\n", characters);
        printf("You typed: '%s'\n", b);
    
        return(0);
    }
    ```
    - 会发现在 `char` 指针做缓冲区的时候, `bufsize` 默认为 `120`, 就算读入缓冲超过 `120` , 也会加倍为`240`. 但是, char 指针可以

      ```
      > ./test
      Type something: dsdsa
      120
      6 characters were read.
      You typed: '����'
      
      > ./test
      Type something: testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt
      240
      130 characters were read.
      You typed: 'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttestt
      '
      ```
    - more via: https://stackoverflow.com/questions/20036074/length-of-line-in-getline-function-c.

## P02

- `.exit`: "meta-commands"
- `strncmp`: the “insert” keyword will be followed by data.


## P03

- storage in memory plan
  - Store rows in blocks of memory called pages
  - Each page stores as many rows as it can fit
  - Rows are serialized into a compact representation with each page
  - Pages are only allocated as needed
  - Keep a fixed-size array of pointers to pages
- [浅析C语言之uint8_t / uint16_t / uint32_t /uint64_t - 知乎](https://zhuanlan.zhihu.com/p/37422763 )

  - 1、这些类型的来源：这些数据类型中都带有_t, _t 表示这些数据类型是通过typedef定义的，而不是新的数据类型。也就是说，它们其实是我们已知的类型的别名。
  - 2、使用这些类型的原因：方便代码的维护。比如，在C中没有bool型，于是在一个软件中，一个程序员使用int，一个程序员使用short，会比较混乱。最好用一个typedef来定义一个统一的bool：
  - 在涉及到跨平台时，不同的平台会有不同的字长，所以利用预编译和typedef可以方便的维护代码。
  - 在C99标准中定义了这些数据类型，具体定义在：`/usr/include/stdint.h` ISO C99: 7.18 Integer types
    ```c
    #ifndef __int8_t_defined
    # define __int8_t_defined
    typedef signed char             int8_t;
    typedef short int               int16_t;
    typedef int                     int32_t;
        # if __WORDSIZE == 64
            typedef long int                int64_t;
        # else
        __extension__
        typedef long long int           int64_t;
        # endif
    #endif
    
    typedef unsigned char           uint8_t;
    typedef unsigned short int      uint16_t;
    
    #ifndef __uint32_t_defined
        typedef unsigned int            uint32_t;
        # define __uint32_t_defined
    #endif
    
    #if __WORDSIZE == 64
        typedef unsigned long int       uint64_t;
    #else
        __extension__
        typedef unsigned long long int  uint64_t;
    #endif
    ```
    - > [When should one use the datatypes from stdint.h?](https://stackoverflow.com/questions/20077313)
      - When the programming tasks specify the integer width especially to accommodate some file or communication protocol format.
      - When high degree of *portability* between platforms is required over *performance*.
    - `uint32_t` means `unsigned int 32 type`. via: https://stackoverflow.com/questions/48833976 & https://stackoverflow.com/questions/231760

- Strcut, Typedef
  ```c
  // via: https://stackoverflow.com/questions/17720223
  truct {
     ...
  } myNameStruct;  // defines myNameStruct as a variable with this struct
                   // definition, but the struct definition cannot be re-used.
  
  struct Name {
     ...
  } myNameStruct;	 // define a struct, and declare/define a struct variable 
  				 // at the same time:
  
  typedef struct {
     ...
  } Name_t;		 // use an untagged struct type inside a typedef:
  
  typedef struct Name {
     ...
  } Name_t;		 // begin with typedef, NewTypeName will be Name_t, 
  				 // not a varible
  ```

- 序列化: 把对象转化为可传输的字节序列过程称为序列化
- 反序列化: 把字节序列还原为对象的过程称为反序列化


## P04 Our First Tests (and Bugs)

- `scanf` has some disadvantages.
  - If the string it’s reading is larger than the buffer it’s reading into, it will cause a buffer overflow and start writing into unexpected places. We want to check the length of each string before we copy it into a Row structure. And to do that, we need to divide the input by spaces.

## Bugs

- [How to use `#pragma GCC diagnostic ignored` to ignore a warning in GCC?](https://stackoverflow.com/questions/1801081/how-to-use-pragma-gcc-diagnostic-ignored-to-ignore-a-warning-in-gcc)
- `1410 is the max number of rows in a table` of `main_spec.rb`

## P05 Persistence to Disk

*“Nothing in the world can take the place of persistence.” –* [Calvin Coolidge](https://en.wikiquote.org/wiki/Calvin_Coolidge)

- To add persistence, we can simply write those blocks of memory to a file, and read them back into memory the next time the program starts up.
  - To make this easier, we’re going to make an abstraction called the pager. We ask the pager for page number x, and the pager gives us back a block of memory. It first looks in its cache. On a cache miss, it copies data from disk into memory (by reading the database file).

- `off_t`:  [c - Where to find the complete definition of off_t type?](https://stackoverflow.com/questions/9073667/where-to-find-the-complete-definition-of-off-t-type )
  - it's a standard. found [The Open Group Base Specifications Issue 7, 2018 edition](https://pubs.opengroup.org/onlinepubs/9699919799/ )
- We assume pages are saved one after the other in the database file: Page 0 at offset 0, page 1 at offset 4096, page 2 at offset 8192, etc. If the requested page lies outside the bounds of the file, we know it should be blank, so we just allocate some memory and return it. The page will be added to the file when we flush the cache to disk later.

## P06 The Cursor Abstraction

- We’re going to add a `Cursor` object which represents a location in the table. Things you might want to do with cursors:
  - Create a cursor at the beginning of the table
  - Create a cursor at the end of the table
  - Access the row the cursor is pointing to
  - Advance the cursor to the next row
- Those are the behaviors we’re going to implement now. Later, we will also want to:
  - Delete the row pointed to by a cursor
  - Modify the row pointed to by a cursor
  - Search a table for a given ID, and create a cursor pointing to the row with that ID

## P07 Introduction to the B-Tree

### B Tree vs B+Tree

|                               | B-tree         | B+ tree             |
| :---------------------------- | :------------- | :------------------ |
| Pronounced                    | “Bee Tree”     | “Bee Plus Tree”     |
| Used to store                 | Indexes        | Tables              |
| Internal nodes store keys     | Yes            | Yes                 |
| Internal nodes store values   | Yes            | No                  |
| Number of children per node   | Less           | More                |
| Internal nodes vs. leaf nodes | Same structure | Different structure |

###  Internal nodes vs leaf nodes

| For an order-m tree… | Internal Node                 | Leaf Node           |
| :------------------- | :---------------------------- | :------------------ |
| Stores               | keys and pointers to children | keys and values     |
| Number of keys       | up to m-1                     | as many as will fit |
| Number of pointers   | number of keys + 1            | none                |
| Number of values     | none                          | number of keys      |
| Key purpose          | used for routing              | paired with value   |
| Stores values?       | No                            | Yes                 |

- The depth of the tree only increases when we split the root node. Every leaf node has the same depth and close to the same number of key/value pairs, so the tree remains balanced and quick to search.

## P08 B-Tree Leaf Node Format

- Nodes need to store some metadata in a header at the beginning of the page. Every node will store what type of node it is, whether or not it is the root node, and a pointer to its parent (to allow finding a node’s siblings)

![](https://cstack.github.io/db_tutorial/assets/images/leaf-node-format.png)
