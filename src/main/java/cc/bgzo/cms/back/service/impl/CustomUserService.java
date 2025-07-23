package cc.bgzo.cms.back.service.impl;

import cc.bgzo.cms.back.entity.SysRole;
import cc.bgzo.cms.back.entity.SysUser;
import cc.bgzo.cms.back.mapper.SysUserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import java.util.ArrayList;
import java.util.List;

/**
 *  * @Description:专门用于security账户验证的服务层
 */

public class CustomUserService implements UserDetailsService {
    @Autowired
    private SysUserMapper sysUserMapper;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        System.out.println(username);
        SysUser user = null;
        try {
            user = sysUserMapper.findUserByName(username);

        }catch (Exception e){
            System.out.println(e.toString());
        }

        if (user != null) {
            List<SysRole> roles = user.getRoles();//获取用户角色
            List<GrantedAuthority> grantedAuthorities = new ArrayList<>();
            for (SysRole role : roles) {
                if (role != null && role.getName() != null) {
                    GrantedAuthority grantedAuthority = new SimpleGrantedAuthority(role.getName());
                    grantedAuthorities.add(grantedAuthority);
                }
            }
            return new User(user.getUsername(), user.getPassword(), grantedAuthorities);
        } else {
            throw new UsernameNotFoundException("admin: " + username + " do not exist!");
        }
    }
}
