## gs-maven Notes


- Define
    ```java
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.springframework</groupId>
        <artifactId>gs-maven</artifactId>
        <packaging>jar</packaging>
        <version>0.1.0</version>

        <properties>
            <maven.compiler.source>1.8</maven.compiler.source>
            <maven.compiler.target>1.8</maven.compiler.target>
        </properties>

        <build>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-shade-plugin</artifactId>
                    <version>3.2.4</version>
                    <executions>
                        <execution>
                            <phase>package</phase>
                            <goals>
                                <goal>shade</goal>
                            </goals>
                            <configuration>
                                <transformers>
                                    <transformer
                                        implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                        <mainClass>hello.HelloWorld</mainClass>
                                    </transformer>
                                </transformers>
                            </configuration>
                        </execution>
                    </executions>
                </plugin>
            </plugins>
        </build>
    </project>
    ```
  - `<modelVersion>`. POM model version (always 4.0.0).
  - `<groupId>`. Group or organization that the project belongs to. Often expressed as an inverted domain name.
  - `<artifactId>`. Name to be given to the project’s library artifact (for example, the name of its JAR or WAR file.
    - artifact 表示某个 module 要如何打包, `war exploded`, `war`, `jar`, `ear` 等等这种打包形式
      - 一个module有了 Artifacts 就可以部署了
  - `<version>`: Version of the project that is being built.
  - `<packaging>`: How the project should be packaged.
    - Defaults to "jar" for JAR file packaging.
    - Use "war" for WAR file packaging.
- When it comes to choosing a **versioning scheme**, Spring recommends the **semantic versioning approach**.
- Build
  - several build lifecycle goals with Maven
    ```shell
    mvn compile # 1. compile the project’s code, than will find class files in in the target/classes directory.
    mvn package # 2. create a library package (such as a JAR file)
    java -jar target/gs-maven-0.1.0.jar
    mvn install # 3. install the library in the local Maven dependency repository(~/.m2/repository).
                # included test.
    mvn test
    ```
- Test
  - Maven uses a plugin called "surefire" to run unit tests. The default configuration of this plugin compiles and runs all classes in `src/test/java` with a name matching `*Test`

