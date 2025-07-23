package cc.bgzo.cms.back.service.impl;

import cc.bgzo.cms.back.entity.SysUser;
import cc.bgzo.cms.back.mapper.SysUserMapper;
import cc.bgzo.cms.back.service.ISysUserService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.apache.tomcat.jni.Global;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
/**
 *  */

@Service
public class SysUserServiceImpl extends ServiceImpl<SysUserMapper, SysUser> implements ISysUserService {
    @Autowired
    private SysUserMapper sysUserMapper;

    @Override
    public void saveSysUser(SysUser sysUser) {
        if (sysUser.getId() != null) {
            sysUserMapper.updateById(sysUser);
        } else {
            //新增用户设置默认密码123456
            String pwd = new BCryptPasswordEncoder().encode("123456");
            sysUser.setPassword(pwd);
            sysUser.setStatus(1);//用户状态
            Integer index = sysUserMapper.insert(sysUser);
        }
        //更新角色
        updateSysUserRoles(sysUser);
    }

    /**
     * 更新用户角色
     */
    private void updateSysUserRoles(SysUser sysUser) {
        if (sysUser != null && sysUser.getRoles() != null) {
            //删除原有角色
            sysUserMapper.deleteRoles(sysUser);
            //更新角色
            sysUserMapper.insertRoles(sysUser);
        }
    }

    @Override
    public SysUser findUserById(Integer userId) {
        return sysUserMapper.findUserById(userId);
    }

    /**
     * 根据 Name 查询用户关联查询角色
     *
     * @param userName
     * @return
     */
    @Override
    public SysUser findUserByName(String userName) {
        return sysUserMapper.findUserByName(userName);
    }

}
