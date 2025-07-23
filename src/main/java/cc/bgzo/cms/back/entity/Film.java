package cc.bgzo.cms.back.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.activerecord.Model;
import lombok.Data;
import lombok.EqualsAndHashCode;
/**
 *  */

@Data
@TableName(value = "film")
@EqualsAndHashCode(callSuper = true)
public class Film extends Model<Film> {
	@TableId(type = IdType.AUTO)
	private Integer id;
	private String filmName;
	private String filmPic;
	private String summary;
	private String actor;
	private String director;
	private String nation;
	private String type;
	private String language;
	private String releaseTime;

	@TableLogic
	private Integer delFlag;
}
