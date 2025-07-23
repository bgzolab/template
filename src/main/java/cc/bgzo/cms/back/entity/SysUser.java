package cc.bgzo.cms.back.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import lombok.Data;

import java.util.Date;
import java.util.List;

/**
 *  */

@Data
public class SysUser {
    @TableId(type = IdType.AUTO)    // NOTE: 主键自动增加
    private Integer id;
    private String  username;        // 登录名
    private String  password;
    private String  name;            // 用户名
    private String  email;
    private String  mobile;
    private Integer status;

//    private String userType;      // 用户类型

    private Integer createBy;
    private Date    createDate;
    private Integer updateBy;
    private Date    updateDate;

    // 逻辑字段
    @TableLogic
    private String  delFlag;

    //角色, mybatis-plus 忽略该属性和数据库的映射
    @TableField(exist = false)
    private List<SysRole> roles;
}
