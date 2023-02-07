package cc.bgzo.leetcode.editor.cn;

import javax.security.auth.kerberos.KeyTab;
import javax.sql.rowset.spi.SyncResolver;
import java.security.Key;
import java.util.*;

public class One604警告一小时内使用相同员工卡大于等于三次的人{
    public static void main(String[] args) {
        Solution solution = new One604警告一小时内使用相同员工卡大于等于三次的人().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public List<String> alertNames(String[] keyName, String[] keyTime) {
        // Group the times by the name of the card user, then sort each group

        Map<String, List<Integer>> hm = new HashMap<>();
        for(int i = 0; i<keyName.length; i++){
            hm.putIfAbsent(keyName[i], new ArrayList<>());

            Integer hour = ( keyTime[i].charAt(0) -'0')* 10 + (keyTime[i].charAt(1) - '0');
            Integer minute = ( keyTime[i].charAt(3) - '0')* 10 + (keyTime[i].charAt(4) - '0');
            System.out.println(hour*60+minute);
            hm.get(keyName[i]).add(hour*60+minute);
        }

        Set<String> keys = hm.keySet();
        Set<String> ans = new HashSet<>();
        for(String key: keys){
            List<Integer> value = hm.get(key);
            Collections.sort(value);

            for(int i = 2; i<value.size(); i++){ // 如果起步 2 越界了会自动停止循环的
                int time1 = value.get(i-2);
                int time2 = value.get(i);
                if(time2-time1 <= 60){
                    ans.add(key);
//                    break;
//                    System.out.println(key);
//                    System.out.println(value);
//                    System.out.println(i);

                }
            }
        }
        List<String> sortedList = new ArrayList<>(ans);
        Collections.sort(sortedList);
        return sortedList;


//        Map<String, List<Integer>> timeMap = new HashMap<String, List<Integer>>();
//        int n = keyName.length;
//        for (int i = 0; i < n; i++) {
//            String name = keyName[i];
//            String time = keyTime[i];
//            timeMap.putIfAbsent(name, new ArrayList<Integer>());
//            int hour = (time.charAt(0) - '0') * 10 + (time.charAt(1) - '0');
//            int minute = (time.charAt(3) - '0') * 10 + (time.charAt(4) - '0');
//            timeMap.get(name).add(hour * 60 + minute);
//        }
//        List<String> res = new ArrayList<String>();
//        Set<String> keySet = timeMap.keySet();
//        for (String name : keySet) {
//            List<Integer> list = timeMap.get(name);
//            Collections.sort(list);
//            int size = list.size();
//            for (int i = 2; i < size; i++) {
//                int time1 = list.get(i - 2), time2 = list.get(i);
//                int difference = time2 - time1;
//                System.out.println(name);
//                System.out.println(list);
//                if (difference <= 60) {
//                    res.add(name);
////                    break;
//                    System.out.println(name);
//                    System.out.println(list);
//                }
//            }
//        }
//        Collections.sort(res);
//        return res;
////
//        作者：LeetCode-Solution
//        链接：https://leetcode.cn/problems/alert-using-same-key-card-three-or-more-times-in-a-one-hour-period/solution/jing-gao-yi-xiao-shi-nei-shi-yong-xiang-ioeiw/
//        来源：力扣（LeetCode）
//        著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
//






//
//        Map<String, List<String>> hm = new hm<>();
//
//
////        List<String> keys = hm.entrySet();
//        Set<String> sets = hm.keySet();
//
//        for(String set: sets){
////            Arrays.sort(hm.get(set));
//            Collections.sort(hm.get(set));
//            System.out.println(hm.get(set));

//        }



// error        ArrayList<String> key_time = (ArrayList<String>) Arrays.asList(keyTime);
// right        ArrayList<String> key_time = new ArrayList<>(Arrays.asList(keyTime));

//        Collections.sort(key_time);
//        System.out.println(key_time);
//        return new ArrayList<>();
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 警告一小时内使用相同员工卡大于等于三次的人
//力扣公司的员工都使用员工卡来开办公室的门。每当一个员工使用一次他的员工卡，安保系统会记录下员工的名字和使用时间。如果一个员工在一小时时间内使用员工卡的次数大
//于等于三次，这个系统会自动发布一个 警告 。 
//
// 给你字符串数组 keyName 和 keyTime ，其中 [keyName[i], keyTime[i]] 对应一个人的名字和他在 某一天 内使用员工卡
//的时间。 
//
// 使用时间的格式是 24小时制 ，形如 "HH:MM" ，比方说 "23:51" 和 "09:49" 。 
//
// 请你返回去重后的收到系统警告的员工名字，将它们按 字典序升序 排序后返回。 
//
// 请注意 "10:00" - "11:00" 视为一个小时时间范围内，而 "23:51" - "00:10" 不被视为一小时内，因为系统记录的是某一天内的使
//用情况。 
//
// 
//
// 示例 1： 
//
// 
//输入：keyName = ["daniel","daniel","daniel","luis","luis","luis","luis"], 
//keyTime = ["10:00","10:40","11:00","09:00","11:00","13:00","15:00"]
//输出：["daniel"]
//解释："daniel" 在一小时内使用了 3 次员工卡（"10:00"，"10:40"，"11:00"）。
// 
//
// 示例 2： 
//
// 
//输入：keyName = ["alice","alice","alice","bob","bob","bob","bob"], keyTime = ["12
//:01","12:00","18:00","21:00","21:20","21:30","23:00"]
//输出：["bob"]
//解释："bob" 在一小时内使用了 3 次员工卡（"21:00"，"21:20"，"21:30"）。
// 
//
// 示例 3： 
//
// 
//输入：keyName = ["john","john","john"], keyTime = ["23:58","23:59","00:01"]
//输出：[]
// 
//
// 示例 4： 
//
// 
//输入：keyName = ["leslie","leslie","leslie","clare","clare","clare","clare"], 
//keyTime = ["13:00","13:20","14:00","18:00","18:51","19:30","19:49"]
//输出：["clare","leslie"]
// 
//
// 
//
// 提示： 
//
// 
// 1 <= keyName.length, keyTime.length <= 10⁵ 
// keyName.length == keyTime.length 
// keyTime 格式为 "HH:MM" 。 
// 保证 [keyName[i], keyTime[i]] 形成的二元对 互不相同 。 
// 1 <= keyName[i].length <= 10 
// keyName[i] 只包含小写英文字母。 
// 
//
// Related Topics 数组 哈希表 字符串 排序 👍 78 👎 0
