package cc.bgzo.cms.back.mapper;

import cc.bgzo.cms.back.entity.SysUser;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;
/**
 *  */

@Repository
@Component
public interface SysUserMapper extends BaseMapper<SysUser> {

    /**
     * find user by username
     * @param username
     * @return
     */
    SysUser findUserByName(String username);

    /**
     * 根据主键获取用户并获取用户角色
     * @param id
     * @return
     */
    SysUser findUserById(Integer id);

    /**
     * 更新角色
     * @param sysUser
     */
    void insertRoles(SysUser sysUser);

    /**
     * 删除角色
     * @param sysUser
     */
    void deleteRoles(SysUser sysUser);


}
