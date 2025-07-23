package cc.bgzo.cms.back.service;

import cc.bgzo.cms.back.entity.SysRole;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;
import java.util.Map;

/**
 *  */
public interface ISysRoleService extends IService<SysRole> {


    void updateRoleDelFlag(SysRole sysRole);

    /**
     * 保存角色
     */
    void saveRole(SysRole sysRole, int[] roleMenus);

    /**
     * 获取角色所管理的菜单
     * @param role
     * @return
     */
    List<Map<String, Object>> getRoleMenuTree(SysRole role);
}
