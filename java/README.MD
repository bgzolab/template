## Trashing
```java
# java
path: \\wsl$\Ubuntu\home\bgzocg\demo\tasks\leetcode\java\src\cc\bgzo
template: $!velocityTool.camelCaseName(${question.frontendQuestionId})$!velocityTool.camelCaseName(${question.title})
package cc.bgzo.leetcode.editor.cn;
public class $!velocityTool.camelCaseName(${question.frontendQuestionId})$!velocityTool.camelCaseName(${question.title}){
    public static void main(String[] args) {
        Solution solution = new $!velocityTool.camelCaseName(${question.frontendQuestionId})$!velocityTool.camelCaseName(${question.title})().new Solution();
    }
    ${question.code}
}
// ${question.title}
${question.content}
```

- 无法自由命名类名
  - > 包的定义与路径无关，为了保护其他文件，固定前缀路径为leetcode/editor/(en|cn)
    > via: via [Issue #509-shuzijun/leetcode-editor](https://github.com/shuzijun/leetcode-editor/issues/509 )
  - 怎么不生成包名? Sucks.
- 题目出现非字母字符的话, 类需要重新命名, 但是提交就又是个问题.
  - 每次本地 debug 需要配置`忽略错误检查`/打入小黑屋...
- 一次只能刷一种题目, 混刷需要反复在设置中切换.

## Contents

| #Tags           | ID                | Mark |
|-----------------|-------------------| ----|
| Bitwise Opera   | Offer001(29)/Offer002(67)/Offer003(338)|     |
| Binary Search   | Offer006(167)/Offer008(209)      | [默写二分](https://labuladong.github.io/algo/1/11/ ) |
| Prefix Sum      | Offer008(209)/Offer010(560)/Offer011(525)/Offer012(724)/Offer013(304) | [秒杀前缀和](https://labuladong.github.io/algo/2/19/23/ )|
| Double Pointer  | Offer006(167)/              | |
| Sliding Windows | Offer008(209)/Offer009(713) | |
| [#nSum](#nsum)  | 18/Offer007(15)        | [秒杀 nSum](https://mp.weixin.qq.com/s/fSyJVvggxHq28a0SdmZm6Q )|
| [#Trie](#trie)  | 208/211/648/677   | [秒杀前缀树算法](https://mp.weixin.qq.com/s/hGrTUmM1zusPZZ0nA9aaNw )|

## nSum

```java
class solution{
    public List<List<Integer>> nSumTarget (List<Integer> nums, int n, int start, int target){
      // via: https://mp.weixin.qq.com/s/fSyJVvggxHq28a0SdmZm6Q
      int size = nums.size();
      List<List<Integer>> res= new ArrayList<>();
      if( n < 2 || size < n) return res;
  
      if( n == 2){
        int lo = start, hi = size -1;
        while (lo<hi){
          int left = nums.get(lo), right = nums.get(hi),
                  sum = left + right;
  
          if(sum < target){
            while (lo < hi && nums.get(lo) == left) lo++;
          } else if( sum > target ){
            while (lo < hi && nums.get(hi) == right) hi--;
          }else {
            res.add(new ArrayList<Integer>(){{add(left); add(right);}});
  
            while (lo < hi && nums.get(lo) == left) lo++;
            while (lo < hi && nums.get(hi)== right) hi--;
          }
        }
      }else{
        for(int i = start; i < size; i++){
          int now = nums.get(i);
          List<List<Integer>> sub =
                  nSumTarget(nums, n-1, i+1, target-now);
  
          for(List<Integer> arr: sub){
            arr.add(now);
            res.add(arr);
          }
  
          while ( i < size-1 && nums.get(i).equals(nums.get(i+1))) i++;
          // while ( i < size && nums.get(i) == now ) i++; 
          // 这样更新i 需要将 for loop 里面的 i 去除
        }
      }
      return res;
    }
}
```

## Trie

### TrieMap

```java
/* 基本的二叉树节点 */
class TreeNode {
  int val;
  TreeNode left, right;
}

// via: https://mp.weixin.qq.com/s/hGrTUmM1zusPZZ0nA9aaNw
/* Trie 树节点实现 */
class TrieNode<V> {
  V val = null;
  TrieNode<V>[] children = new TrieNode[256];
}
class TrieMap<V> {
    // ASCII 码个数
    private static final int R = 256;
    // 当前存在 Map 中的键值对个数
    private int size = 0;
    // Trie 树的根节点
    private TrieNode<V> root = null;

    private static class TrieNode<V> {
        V val = null;
        TrieNode<V>[] children = new TrieNode[R];
    }

    /***** 增/改 *****/

    // 在 map 中添加或修改键值对
    public void put(String key, V val) {
        if (!containsKey(key)) {
            // 新增键值对
            size++;
        }
        // 需要一个额外的辅助函数，并接收其返回值
        root = put(root, key, val, 0);
    }

    // 定义：向以 node 为根的 Trie 树中插入 key[i..]，返回插入完成后的根节点
    private TrieNode<V> put(TrieNode<V> node, String key, V val, int i) {
        if (node == null) {
            // 如果树枝不存在，新建
            node = new TrieNode<>();
        }
        if (i == key.length()) {
            // key 的路径已插入完成，将值 val 存入节点
            node.val = val;
            return node;
        }
        char c = key.charAt(i);
        // 递归插入子节点，并接收返回值
        node.children[c] = put(node.children[c], key, val, i + 1);
        return node;
    }

    /***** 删 *****/

    // 在 Map 中删除 key
    public void remove(String key) {
        if (!containsKey(key)) {
            return;
        }
        // 递归修改数据结构要接收函数的返回值
        root = remove(root, key, 0);
        size--;
    }

    // 定义：在以 node 为根的 Trie 树中删除 key[i..]，返回删除后的根节点
    private TrieNode<V> remove(TrieNode<V> node, String key, int i) {
        if (node == null) {
            return null;
        }
        if (i == key.length()) {
            // 找到了 key 对应的 TrieNode，删除 val
            node.val = null;
        } else {
            char c = key.charAt(i);
            // 递归去子树进行删除
            node.children[c] = remove(node.children[c], key, i + 1);
        }
        // 后序位置，递归路径上的节点可能需要被清理
        if (node.val != null) {
            // 如果该 TireNode 存储着 val，不需要被清理
            return node;
        }
        // 检查该 TrieNode 是否还有后缀
        for (int c = 0; c < R; c++) {
            if (node.children[c] != null) {
                // 只要存在一个子节点（后缀树枝），就不需要被清理
                return node;
            }
        }
        // 既没有存储 val，也没有后缀树枝，则该节点需要被清理
        return null;
    }

    /***** 查 *****/

    // 搜索 key 对应的值，不存在则返回 null
    public V get(String key) {
        // 从 root 开始搜索 key
        TrieNode<V> x = getNode(root, key);
        if (x == null || x.val == null) {
            // x 为空或 x 的 val 字段为空都说明 key 没有对应的值
            return null;
        }
        return x.val;
    }

    // 判断 key 是否存在在 Map 中
    public boolean containsKey(String key) {
        return get(key) != null;
    }

    // 判断是和否存在前缀为 prefix 的键
    public boolean hasKeyWithPrefix(String prefix) {
        // 只要能找到一个节点，就是存在前缀
        return getNode(root, prefix) != null;
    }

    // NOTE: 在所有键中寻找 query 的最短前缀
    public String shortestPrefixOf(String query) {
        TrieNode<V> p = root;
        // 从节点 node 开始搜索 key
        for (int i = 0; i < query.length(); i++) {
            if (p == null) {
                // 无法向下搜索
                return "";
            }
            if (p.val != null) {
                // 找到一个键是 query 的前缀
                return query.substring(0, i);
            }
            // 向下搜索
            char c = query.charAt(i);
            p = p.children[c];
        }

        if (p != null && p.val != null) {
            // NOTE: 循环结束还需要检查一下
            // 如果 query 本身就是一个键
            return query;
        }
        return "";
    }

    // NOTE:在所有键中寻找 query 的最长前缀
    public String longestPrefixOf(String query) {
        TrieNode<V> p = root;
        // 记录前缀的最大长度
        int max_len = 0;

        // 从节点 node 开始搜索 key
        for (int i = 0; i < query.length(); i++) {
            if (p == null) {
                // 无法向下搜索
                break;
            }
            if (p.val != null) {
                // 找到一个键是 query 的前缀，更新前缀的最大长度
                max_len = i;
            }
            // 向下搜索
            char c = query.charAt(i);
            p = p.children[c];
        }

        if (p != null && p.val != null) {
            // 如果 query 本身就是一个键
            return query;
        }
        return query.substring(0, max_len);
    }

    // NOTE: 搜索前缀为 prefix 的所有键
    public List<String> keysWithPrefix(String prefix) {
        List<String> res = new LinkedList<>();
        // 找到匹配 prefix 在 Trie 树中的那个节点
        TrieNode<V> x = getNode(root, prefix);
        if (x == null) {
            return res;
        }
        // DFS 遍历以 x 为根的这棵 Trie 树
        traverse(x, new StringBuilder(prefix), res);
        return res;
    }

    // NOTE: 遍历以 node 节点为根的 Trie 树，找到所有键
    private void traverse(TrieNode<V> node, StringBuilder path, List<String> res) {
        if (node == null) {
            // 到达 Trie 树底部叶子结点
            return;
        }

        if (node.val != null) {
            // 找到一个 key，添加到结果列表中
            res.add(path.toString());
        }

        // 回溯算法遍历框架
        for (char c = 0; c < R; c++) {
            // 做选择
            path.append(c);
            traverse(node.children[c], path, res);
            // 撤销选择
            path.deleteCharAt(path.length() - 1);
        }
    }

    // NOTE:通配符 . 匹配任意字符
    public List<String> keysWithPattern(String pattern) {
        List<String> res = new LinkedList<>();
        traverse(root, new StringBuilder(), pattern, 0, res);
        return res;
    }

    // 遍历函数，尝试在「以 node 为根的 Trie 树中」匹配 pattern[i..]
    private void traverse(TrieNode<V> node, StringBuilder path, String pattern, int i, List<String> res) {
        if (node == null) {
            // 树枝不存在，即匹配失败
            return;
        }
        if (i == pattern.length()) {
            // pattern 匹配完成
            if (node.val != null) {
                // 如果这个节点存储着 val，则找到一个匹配的键
                res.add(path.toString());
            }
            return;
        }
        char c = pattern.charAt(i);
        if (c == '.') {
            // pattern[i] 是通配符，可以变化成任意字符
            // 多叉树（回溯算法）遍历框架
            for (char j = 0; j < R; j++) {
                path.append(j);
                traverse(node.children[j], path, pattern, i + 1, res);
                path.deleteCharAt(path.length() - 1);
            }
        } else {
            // pattern[i] 是普通字符 c
            path.append(c);
            traverse(node.children[c], path, pattern, i + 1, res);
            path.deleteCharAt(path.length() - 1);
        }
    }

    // 判断是和否存在前缀为 prefix 的键
    public boolean hasKeyWithPattern(String pattern) {
        // 从 root 节点开始匹配 pattern[0..]
        return hasKeyWithPattern(root, pattern, 0);
    }

    // 函数定义：从 node 节点开始匹配 pattern[i..]，返回是否成功匹配
    private boolean hasKeyWithPattern(TrieNode<V> node, String pattern, int i) {
        if (node == null) {
            // 树枝不存在，即匹配失败
            return false;
        }
        if (i == pattern.length()) {
            // 模式串走到头了，看看匹配到的是否是一个键
            return node.val != null;
        }
        char c = pattern.charAt(i);
        // 没有遇到通配符
        if (c != '.') {
            // 从 node.children[c] 节点开始匹配 pattern[i+1..]
            return hasKeyWithPattern(node.children[c], pattern, i + 1);
        }
        // 遇到通配符
        for (int j = 0; j < R; j++) {
            // pattern[i] 可以变化成任意字符，尝试所有可能，只要遇到一个匹配成功就返回
            if (hasKeyWithPattern(node.children[j], pattern, i + 1)) {
                return true;
            }
        }
        // 都没有匹配
        return false;
    }

    // 从节点 node 开始搜索 key，如果存在返回对应节点，否则返回 null
    // 就算getNode(key)的返回值x非空，也只能说字符串key是一个「前缀」
    // 除非x.val同时非空，才能判断键key存在
    private TrieNode<V> getNode(TrieNode<V> node, String key) {
        TrieNode<V> p = node;
        // 从节点 node 开始搜索 key
        for (int i = 0; i < key.length(); i++) {
            if (p == null) {
                // 无法向下搜索
                return null;
            }
            // 向下搜索
            char c = key.charAt(i);
            p = p.children[c];
        }
        return p;
    }

    public int size() {
        return size;
    }
}

class Trie {
    // 直接封装 TrieSet
    TrieSet set = new TrieSet();

    // 插入一个元素
    public void insert(String word) {
        set.add(word);
    }

    // 判断元素是否在集合中
    public boolean search(String word) {
        return set.contains(word);
    }

    // 判断集合中是否有前缀为 prefix 的元素
    public boolean startsWith(String prefix) {
        return set.hasKeyWithPrefix(prefix);
    }
}

class TrieSet {
    // 底层用一个 TrieMap，键就是 TrieSet，值仅仅起到占位的作用
    // 值的类型可以随便设置，我参考 Java 标准库设置成 Object
    private final TrieMap<Object> map = new TrieMap<>();

    /***** 增 *****/

    // 在集合中添加元素 key
    public void add(String key) {
        map.put(key, new Object());
    }

    /***** 删 *****/

    // 从集合中删除元素 key
    public void remove(String key) {
        map.remove(key);
    }

    /***** 查 *****/

    // 判断元素 key 是否存在集合中
    public boolean contains(String key) {
        return map.containsKey(key);
    }

    // 在集合中寻找 query 的最短前缀
    public String shortestPrefixOf(String query) {
        return map.shortestPrefixOf(query);
    }

    // 在集合中寻找 query 的最长前缀
    public String longestPrefixOf(String query) {
        return map.longestPrefixOf(query);
    }

    // 在集合中搜索前缀为 prefix 的所有元素
    public List<String> keysWithPrefix(String prefix) {
        return map.keysWithPrefix(prefix);
    }

    // 判断集合中是否存在前缀为 prefix 的元素
    public boolean hasKeyWithPrefix(String prefix) {
        return map.hasKeyWithPrefix(prefix);
    }

    // 通配符 . 匹配任意字符，返回集合中匹配 pattern 的所有元素
    public List<String> keysWithPattern(String pattern) {
        return map.keysWithPattern(pattern);
    }

    // 通配符 . 匹配任意字符，判断集合中是否存在匹配 pattern 的元素
    public boolean hasKeyWithPattern(String pattern) {
        return map.hasKeyWithPattern(pattern);
    }

    // 返回集合中元素的个数
    public int size() {
        return map.size();
    }
}
```

