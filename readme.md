# Make Demo 

No idea for VS and Clion to complier a cpp project. So even though having learnt coding 2 years I still not know how to write a makefile. So wirte a demo to learn again.


# make VS cmake VS nmake

- make: 相当于智能批处理工具, 本身并没有编译和链接的功能, 而是用类似于批处理的方式 -> 通过**调用 makefile 中用户指定的命令**来进行编译和链接的. 
- makefile: 文件**包含调用 gcc(编译器)编译某个源文件的命令**. makefile在简单的工程可手写, 但是当工程非常大的时候, 就会很复杂.
- cmake: 根据一个叫 `CMakeLists.txt` 文件(组态档)跨平台生成对应平台能用的makefile.

> Make (or rather a Makefile) is a buildsystem - it drives the compiler and other build tools to build your code.
> 
> CMake is a generator of buildsystems. It can produce Makefiles, it can produce Ninja build files, it can produce KDEvelop or Xcode projects, it can produce Visual Studio solutions. From the same starting point, the same CMakeLists.txt file. So if you have a platform-independent project, CMake is a way to make it buildsystem-independent as well.
> 
> If you have Windows developers used to Visual Studio and Unix developers who swear by GNU Make, CMake is (one of) the way(s) to go.
> 
> I would always recommend using CMake (or another buildsystem generator, but CMake is my personal preference) if you intend your project to be multi-platform or widely usable. CMake itself also provides some nice features like dependency detection, library interface management, or integration with CTest, CDash and CPack.
>
> Using a buildsystem generator makes your project more future-proof. Even if you're GNU-Make-only now, what if you later decide to expand to other platforms (be it Windows or something embedded), or just want to use an IDE?
> 
> via https://stackoverflow.com/questions/25789644/difference-between-using-makefile-and-cmake-to-compile-the-code/25790020#25790020

- nmake: `Microsoft Visual Studio` 附带命令, 需VS, 实际上可以说相当于 linux 的 make.


# Reference

1. Linux下C语言编程实践(Makefile入门), 张齐勋,  https://mp.weixin.qq.com/s/TbiaacY3h8SutWVNeNEdeQ
