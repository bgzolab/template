package cc.bgzo.cms.back.web;

import cc.bgzo.cms.back.entity.SysMenu;
import cc.bgzo.cms.back.service.IFilmService;
import cc.bgzo.cms.back.service.ISysMenuService;
import cc.bgzo.cms.back.service.ISysRoleService;
import cc.bgzo.cms.back.service.ISysUserService;
import cc.bgzo.cms.back.service.impl.FilmServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

/**
 *  */

@Controller
@RequestMapping("/a")
public class SysIndexController {
    @Autowired
    private ISysMenuService sysMenuService;
    @Autowired
    private ISysUserService sysUserService;
    @Autowired
    private ISysRoleService sysRoleService;
    @Autowired
    private IFilmService iFilmService;

    /**
     * 读取当前登录成功用户的角色，并根据角色加载菜单
     * @param model
     * @return
     */
    @RequestMapping("/index")
    public String index(Model model) {
        // 获得spring security用户
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext()
                .getAuthentication()
                .getPrincipal();

        // 读取当前用户管理的菜单
        List<SysMenu> menuList = sysMenuService.findListByName(userDetails.getUsername());

//        menuList.forEach(System.out::println);

        // 获取当前登录的系统用户
        model.addAttribute("menus",menuList);

        return "sys/index";
    }

    /**
     * 读取控制台数据
     */
    @RequestMapping("/console")
    public String console(Model model) {

        /**
         * 用户数, 角色数, 菜单数, 电影数
         */
        Integer userCount = sysUserService.count();
        Integer roleCount = sysRoleService.count();
        Integer menuCount = sysMenuService.count();
        Integer filmCount = iFilmService.count();

        model.addAttribute("userCount", userCount);
        model.addAttribute("roleCount", roleCount);
        model.addAttribute("menuCount", menuCount);
        model.addAttribute("filmCount", filmCount);

        return "sys/console";
    }
}
