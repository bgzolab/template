package cc.bgzo.cms.back.mapper;

import cc.bgzo.cms.back.entity.SysMenu;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.io.Serializable;
import java.util.Collection;
import java.util.List;


/**
 *  */

@Repository
public interface SysMenuMapper extends BaseMapper<SysMenu> {

    /**
     * 根据用户名获取对应的菜单
     * @param username
     * @return
     */
    List<SysMenu> findByUserName(@Param("username") String username);

}
