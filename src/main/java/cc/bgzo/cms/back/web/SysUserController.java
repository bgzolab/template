package cc.bgzo.cms.back.web;

import cc.bgzo.cms.back.entity.SysRole;
import cc.bgzo.cms.back.entity.SysUser;
import cc.bgzo.cms.back.service.ISysRoleService;
import cc.bgzo.cms.back.service.ISysUserService;
import cc.bgzo.cms.vo.ResponseResult;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;

/**
 *  */

@Controller
@RequestMapping(value = "/a/user")
public class SysUserController {
    @Autowired
    private ISysUserService sysUserService;
    @Autowired
    private ISysRoleService sysRoleService;

    //请求登录
    @RequestMapping("/login")
    public String login() {
        return "sys/login";
    }

    @RequestMapping("/logout")
    public String loginPage(HttpServletRequest request, HttpServletResponse response) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null) {
            //设置用户厉害
            new SecurityContextLogoutHandler().logout(request, response,auth);
        }
        return "redirect:/a/user/login";
    }

    //加载用户列表数据
    @RequestMapping("/list")
    public String list(Integer curr, Integer size, SysUser sysUser, Model model) {
        /**
         * 默认配置 :
         * 前台传递的 页码 和 每页记录数
         */
        Integer current = 1;
        Integer pageSize = 2;
        if (curr != null) current = curr;
        if (size != null) pageSize = size;


        //查询用户的数据，并分页
        //列表数据，总记录数，当前页
        //分页对象
        //查询对象
        QueryWrapper<SysUser> queryWrapper = new QueryWrapper<>();

        /**
         * 绑定查询条件
         */
        if (sysUser != null && sysUser.getUsername() != null && sysUser.getUsername() != "") {
            queryWrapper.eq("username",sysUser.getUsername());
        }
        if (sysUser != null && sysUser.getEmail() != null && sysUser.getEmail() != "") {
            queryWrapper.eq("email",sysUser.getEmail());
        }

        IPage<SysUser> page = sysUserService.page(new Page<>(current, pageSize), queryWrapper);

        /**
         * 获取某一页的记录数
         */
        model.addAttribute("userList",page.getRecords());

        /**
         * 获取记录总数
         */
        model.addAttribute("total",page.getTotal());

        /**
         * 当前页
         */
        model.addAttribute("current",page.getCurrent());

        return "sys/userList";
    }

    /**
     * 编辑
     */
    @RequestMapping("/form")
    public String form(Model model, Integer id, SysUser sysUser) {
        //获取所有的角色
        List<SysRole> roleList = sysRoleService.list();
        if (id != null) {
            sysUser = sysUserService.findUserById(id);
        }
        model.addAttribute("roleList", roleList);
        System.out.println(sysUser);
        model.addAttribute("sysUser", sysUser);
        return "sys/userForm";
    }

    @ResponseBody
    @RequestMapping("/save")
    public String save(SysUser sysUser) {
        if(sysUserService.findUserByName(sysUser.getUsername()) == null){
            sysUserService.saveSysUser(sysUser);
            System.out.println("save user successfully!");

        } else{
            System.out.println("add failed!");
            return "error";
        }
        return "success";
    }

    /**
     * 修改密码
     */
    @RequestMapping("/modify")
    public String modify(Model model) {
        UserDetails userDetails = (UserDetails) SecurityContextHolder.getContext()
                .getAuthentication()
                .getPrincipal();

        QueryWrapper<SysUser> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("username",userDetails.getUsername());
        SysUser sysUser = sysUserService.getOne(queryWrapper);

        /**
         * 将用户保存到 model
         */
        model.addAttribute("sysUser",sysUser);
        return "sys/modifyUserPwd";
    }

    /**
     * 保存修改吗
     * @param sysUser
     * @return
     */
    @ResponseBody
    @RequestMapping("/modifySubmit")
    public String modifySubmit(SysUser sysUser){
        System.out.println(sysUser);

        /**
         * NOTE: 此时 sysUser.password 是明文，需要转成密文
         */
        String pwd = new BCryptPasswordEncoder().encode(sysUser.getPassword());
        sysUser.setPassword(pwd);

        sysUserService.saveOrUpdate(sysUser);

        return "success";
    }

    /**
     * 修改用户的状态
     */
    @ResponseBody
    @RequestMapping("/changeStatus")
    public ResponseResult changeStatus(SysUser sysUser) {
        sysUserService.updateById(sysUser);
        ResponseResult result = null;
        if (sysUser.getStatus() == 2) {
            result = new ResponseResult("200","账户已锁定");
        } else {
            result = new ResponseResult("200","账户已启动");
        }
        return result;
    }

}
