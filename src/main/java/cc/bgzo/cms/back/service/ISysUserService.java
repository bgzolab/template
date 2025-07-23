package cc.bgzo.cms.back.service;

import cc.bgzo.cms.back.entity.SysUser;
import com.baomidou.mybatisplus.extension.service.IService;
/**
 *  */

public interface ISysUserService extends IService<SysUser> {

    /**
     * 保存用户
     * @param sysUser
     */
    void saveSysUser(SysUser sysUser);

    /**
     * 根据id查询用户关联查询角色
     * @param userId
     * @return
     */
    SysUser findUserById(Integer userId);

    /**
     * 根据 Name 查询用户关联查询角色
     * @param userName
     * @return
     */
    SysUser findUserByName(String userName);
}
