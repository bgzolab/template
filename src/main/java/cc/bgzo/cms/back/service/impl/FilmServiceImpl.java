package cc.bgzo.cms.back.service.impl;

import cc.bgzo.cms.back.entity.Film;
import cc.bgzo.cms.back.mapper.FilmMapper;
import cc.bgzo.cms.back.service.IFilmService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 *  */

@Service
public class FilmServiceImpl extends ServiceImpl<FilmMapper, Film> implements IFilmService {
}
