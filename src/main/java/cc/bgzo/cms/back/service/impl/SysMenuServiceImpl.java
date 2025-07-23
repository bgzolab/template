package cc.bgzo.cms.back.service.impl;

import cc.bgzo.cms.back.entity.SysMenu;
import cc.bgzo.cms.back.mapper.SysMenuMapper;
import cc.bgzo.cms.back.service.ISysMenuService;
import cc.bgzo.cms.vo.ResponseResult;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.CollectionUtils;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 *  */


@Service
public class SysMenuServiceImpl extends ServiceImpl<SysMenuMapper, SysMenu> implements ISysMenuService {
    @Autowired
    private SysMenuMapper sysMenuMapper;

    @Override
    public List<SysMenu> findListByName(String username) {
        return sysMenuMapper.findByUserName(username);
    }

    public List<Map<String, Object>> queryMenuTree() {
        List<SysMenu> sysMenus = sysMenuMapper.selectList(new QueryWrapper<SysMenu>());

        // rootMenu存放根菜单
        List<Map<String, Object>> rootMenu = new ArrayList<>();
        //取出pid为0的节点
        if (!CollectionUtils.isEmpty(sysMenus)) {
            List<SysMenu> parentList = sysMenus
                    .stream().filter(item -> 0 == (item.getPid())).collect(Collectors.toList());
            //把根节点放在Mpa里面，并去调用递归算法去查询子树
            if (!CollectionUtils.isEmpty(parentList)) {
                parentList.forEach(item -> {
                    Map<String, Object> map = new HashMap<>();
                    packageData(item, map);
                    //查询出子节点
                    this.querySubMenuTree(map, sysMenus);
                    rootMenu.add(map);
                });
            }

        }
        return rootMenu;
    }

    /**
     * 获取子菜单
     */
    public Map<String, Object> querySubMenuTree(Map<String, Object> rootMap, List<SysMenu> sysMenus) {
        //subMenu
        List<Map<String, Object>> subMenu = new ArrayList<>();

        //选出某一个根节点下面的子树，递归。
        List<SysMenu> sub = sysMenus
                .stream().filter(item -> rootMap.get("id") == (item.getPid())).collect(Collectors.toList());
                //取出pid为0的节点
        if (!sub.isEmpty()) {
            sub.forEach(item -> {
                Map<String, Object> subMap = new HashMap<>();
                packageData(item, subMap);
                //查询出子节点
                subMenu.add(subMap);
                this.querySubMenuTree(subMap, sysMenus);
            });
        }

        if (!CollectionUtils.isEmpty(subMenu)) {
            rootMap.put("children", subMenu);
        }
        return rootMap;
    }

    /**
     * 封装菜单数据
     *
     * @param sysMenu
     * @param map
     */
    private void packageData(SysMenu sysMenu, Map<String, Object> map) {
        map.put("id", sysMenu.getId());
        map.put("name", sysMenu.getName());
        map.put("href", sysMenu.getUrl());
//        map.put("sort", sysMenu.getSort());
    }

    public SysMenu queryMenuById(Integer menuId) {
        return sysMenuMapper.selectById(menuId);
    }

    /**
     * 获取父级菜单
     * @param menuId
     * @return
     */
    public SysMenu queryParentMenuById(Integer menuId) {
        SysMenu sysMenu = sysMenuMapper.selectById(menuId);
        return sysMenuMapper.selectList(new QueryWrapper<SysMenu>()
                .eq("id", sysMenu.getPid() == 0 ? menuId : sysMenu.getPid())).get(0);
    }

    /**
     *  保存
     * @param sysMenu
     */
    public void saveMenu(SysMenu sysMenu) {
        if (sysMenu.getId() != null) {
            sysMenuMapper.updateById(sysMenu);
        } else {
            if (sysMenu.getPid() == null) {
                sysMenu.setPid(0);
            }
            sysMenuMapper.insert(sysMenu);
        }
    }

    /**
     * 删除菜单
     * @param menuId
     * @return
     */
    public ResponseResult deleteMenu(Integer menuId) {
        //查询是否含有子菜单，有则删除失败
        List<SysMenu> subCatalog = sysMenuMapper.selectList(new QueryWrapper<SysMenu>()
                .eq("pid", menuId));
        if (!subCatalog.isEmpty()) {
            return new ResponseResult("201", "请先删除子菜单！");
        }

        //开始删除菜单
        sysMenuMapper.deleteById(menuId);

        return new ResponseResult("200", "删除成功！");
    }
}
