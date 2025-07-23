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
public class SysRole {
    @TableId(type = IdType.AUTO)
    private Integer id;
    private String name;
    private String remark;

    private Integer createBy;
    private Date createDate;//创建时间
    private Integer updateBy;
    private Date updateDate;//更新时间

    @TableLogic
    private String delFlag;

    @TableField(exist = false)
    private List<SysMenu> menus;
}
