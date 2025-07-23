package cc.bgzo.cms.back.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

import java.io.Serializable;
import java.time.LocalDateTime;
/**
 *  */

@Data
@EqualsAndHashCode(callSuper = false)
@Accessors(chain = true)
public class SysDict implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(value = "id", type = IdType.AUTO)
    private Integer id;

    /**
     * 类型
     */
    private String typeCode;

    /**
     * 字典名
     */
    private String value;

    /**
     * 字典值
     */
    private String label;

    private String description;

    private LocalDateTime createDate;

    private Integer createBy;

    private LocalDateTime updateDate;

    private Integer updateBy;

    @TableLogic
    private String delFlag;

}
