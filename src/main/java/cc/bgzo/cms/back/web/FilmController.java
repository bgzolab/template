package cc.bgzo.cms.back.web;

import cc.bgzo.cms.back.entity.Film;
import cc.bgzo.cms.back.entity.SysDict;
import cc.bgzo.cms.back.service.IFilmService;
import cc.bgzo.cms.back.service.ISysDictService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 *  */

@Controller
@RequestMapping("/a/film")
public class FilmController {
    @Autowired
    private IFilmService filmService;
    @Autowired
    private ISysDictService sysDictService;

    @ModelAttribute("film")
    public Film get(Integer id) {
        if (id != null){
            return filmService.getById(id);
        }else{
            return new Film();
        }
    }

    @RequestMapping("/list")
    public String list() {
        return "film/filmList";
    }

    /**
     * 异步返回列表数据
     * @return
     */
    @ResponseBody
    @RequestMapping("/getListData")
    public Map<String, Object> getListData(Integer pageIndex, Integer pageSize) {
        Map<String,Object> map = new HashMap<>();
        QueryWrapper<Film> queryWrapper = new QueryWrapper<>();

        IPage<Film> filmIPage = filmService.page(new Page<>(pageIndex,pageSize),queryWrapper);

        map.put("data",filmIPage.getRecords());
        map.put("count",filmIPage.getTotal());

        return map;
    }


    @RequestMapping("/form")
    public String form(Film film, Model model) {

        List<SysDict> typeDicts = sysDictService.list(new QueryWrapper<SysDict>()
                .eq("type_code","filmtype"));
        List<SysDict> lnDicts = sysDictService.list(new QueryWrapper<SysDict>()
                .eq("type_code","language"));

        model.addAttribute("film", film);
        model.addAttribute("typeDicts", typeDicts);
        model.addAttribute("lnDicts", lnDicts);

        return "film/filmForm";
    }

    @ResponseBody
    @RequestMapping("/save")
    public String save(Film film) {
        filmService.saveOrUpdate(film);
        return "success";
    }

    /**
     * 删除
     */
    @ResponseBody
    @RequestMapping("/delete")
    public String delete(Film film) {
        filmService.removeById(film.getId());
        return "success";
    }

}
