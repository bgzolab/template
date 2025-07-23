package cc.bgzo.cms.back.web;

import cc.bgzo.cms.back.entity.SysMenu;
import cc.bgzo.cms.back.service.ISysMenuService;
import cc.bgzo.cms.vo.ResponseResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;
import java.util.Map;

/**
 *  */

@Controller
@RequestMapping("/a/menu")
public class SysMenuController {
    @Autowired
    private ISysMenuService sysMenuService;

    @RequestMapping("/list")
    public String list() {
        return "sys/menuList";
    }

    @ResponseBody
    @RequestMapping("/queryMenuTree")
    public List<Map<String, Object>> queryMenuTree() {
        List<Map<String, Object>> map = sysMenuService.queryMenuTree();
        return map;
    }

    @ResponseBody
    @RequestMapping("/getMenuById")
    public SysMenu getMenuById(Integer menuId) {
        SysMenu sysMenu = sysMenuService.queryMenuById(menuId);
        return sysMenu;
    }

    @RequestMapping("/getParentMenu")
    @ResponseBody
    public SysMenu getParentMenu(Integer menuId) {
        SysMenu sysMenu = sysMenuService.queryParentMenuById(menuId);
        return sysMenu;
    }

    @RequestMapping("/form")
    public String form() {
        return "menuForm";
    }

    @RequestMapping("/save")
    @ResponseBody
    public String save(SysMenu sysMenu) {
        sysMenuService.saveMenu(sysMenu);
        return "success";
    }

    @RequestMapping("/delete")
    @ResponseBody
    public ResponseResult delete(Integer menuId) {
        return sysMenuService.deleteMenu(menuId);
    }
}
