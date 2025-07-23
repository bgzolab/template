package cc.bgzo.cms.back.service.impl;

import cc.bgzo.cms.back.entity.SysMenu;
import cc.bgzo.cms.back.entity.SysRole;
import cc.bgzo.cms.back.mapper.SysMenuMapper;
import cc.bgzo.cms.back.mapper.SysRoleMapper;
import cc.bgzo.cms.back.service.ISysRoleService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 *  */

@Service
public class SysRoleServiceImpl extends ServiceImpl<SysRoleMapper, SysRole> implements ISysRoleService {
    @Autowired
    private SysRoleMapper sysRoleMapper;
    @Autowired
    private SysMenuMapper sysMenuMapper;

    //查询当前角色所拥有的菜单
    List<SysMenu> roleMenu = null;

    @Override
    public void updateRoleDelFlag(SysRole sysRole) {
        sysRoleMapper.updateRoleDelFlag(sysRole);
    }

    @Override
    public void saveRole(SysRole sysRole, int[] roleMenus) {
        if (sysRole.getId() != null) {
            sysRoleMapper.updateById(sysRole);
        } else {
            sysRoleMapper.insert(sysRole);
        }

        //更新授权
        sysRoleMapper.deleteRoleMenus(sysRole);
        List<SysMenu> roleMenuList = new ArrayList<>();
        for (int i = 0; i < roleMenus.length; i++) {
            SysMenu sysMenu = new SysMenu();
            sysMenu.setId(roleMenus[i]);
            roleMenuList.add(sysMenu);
        }
        sysRole.setMenus(roleMenuList); //给当前角色绑定对应菜单
        sysRoleMapper.insertRoleMenus(sysRole);
    }


    public List<Map<String, Object>> getRoleMenuTree(SysRole role) {
        //查询出所有的菜单
        List<SysMenu> sysMenus = sysMenuMapper.selectList(new QueryWrapper<>());

        //查询当前角色所拥有的菜单
        if (role != null && role.getId() != null) {
            SysRole currRole = sysRoleMapper.findRoleAndMenu(role.getId());
            roleMenu = currRole.getMenus();
        } else {
            roleMenu = new ArrayList<>();
        }

        //rootMenu存放根菜单
        List<Map<String, Object>> rootMenu = new ArrayList<>();

        if (!CollectionUtils.isEmpty(sysMenus)) {

            /**
             * 取出 pid 为 0 的节点, 根节点放在 Map 里面，并去调用递归算法去查询子树
             */
            List<SysMenu> parentList = sysMenus
                    .stream().filter(item -> 0 == (item.getPid())).collect(Collectors.toList());

            if (!CollectionUtils.isEmpty(parentList)) {
                parentList.forEach(item -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("title", item.getName());
                    map.put("value", item.getId());
                    if (!roleMenu.isEmpty()) {
                        roleMenu.forEach(rMenu -> {
                            if (rMenu.getId() == (item.getId())) {
                                map.put("checked", true);
                            }
                        });
                    }

                    //查询出子节点
                    this.querySubMenuTree(map, sysMenus, roleMenu);
                    rootMenu.add(map);
                });
            }

        }
        return rootMenu;
    }


    /**
     * 获取子菜单
     */
    public Map<String, Object> querySubMenuTree(Map<String, Object> rootMap, List<SysMenu> sysMenus, List<SysMenu> roleMenu) {
        //subMenu
        List<Map<String, Object>> subMenu = new ArrayList<>();

        //选出某一个根节点下面的子树，递归。
        List<SysMenu> sub = sysMenus
                .stream().filter(item -> rootMap.get("value") == (item.getPid())).collect(Collectors.toList());
        //取出pid为0的节点
        if (!sub.isEmpty()) {
            sub.forEach(item -> {
                Map<String, Object> subMap = new HashMap<>();
                subMap.put("title", item.getName());
                subMap.put("value", item.getId());
                subMap.put("data", new ArrayList<>());
                if (!roleMenu.isEmpty()) {
                    roleMenu.forEach(rMenu -> {
                        if (rMenu.getId() == (item.getId())) {
                            subMap.put("checked", true);
                        }
                    });
                }
                //查询出子节点
                subMenu.add(subMap);
                this.querySubMenuTree(subMap, sysMenus, roleMenu);
            });
        }

        if (!CollectionUtils.isEmpty(subMenu)) {
            rootMap.put("data", subMenu);
        } else {
            rootMap.put("data", new ArrayList<>());
        }
        return rootMap;
    }
}
