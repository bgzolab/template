package cc.bgzo.cms.back.service;

import cc.bgzo.cms.back.entity.SysMenu;
import cc.bgzo.cms.vo.ResponseResult;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;
import java.util.Map;

/**
 *  */


public interface ISysMenuService extends IService<SysMenu> {
    /**
     * 根据用户名获取对应菜单
     * @param username
     * @return
     */
    List<SysMenu> findListByName(String username);

    /**
     * 以树状形式获取菜单
     * @return
     */
    List<Map<String, Object>> queryMenuTree();

    /**
     *
     * @param menuId
     * @return
     */
    SysMenu queryMenuById(Integer menuId);

    /**
     *
     * @param menuId
     * @return
     */
    SysMenu queryParentMenuById(Integer menuId);

    /**
     * 保存菜单
     * @param sysMenu
     */
    void saveMenu(SysMenu sysMenu);

    /**
     * 删除菜单
     * @param menuId
     * @return
     */
    ResponseResult deleteMenu(Integer menuId);
}
