package cc.bgzo.cms.config;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 *  * @Description:MVC的配置类
 */

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    //默认的访问页面 /user/index
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addRedirectViewController("/a","/a/user/login");//后台路径
        registry.addRedirectViewController("/f","/f/film/index");//前台路径
    }

    //配置图片的访问路径
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        //访问路径： http://localhost:9000/cms/public/film/xxx.jpg
        registry.addResourceHandler("/public/**")
                .addResourceLocations("file:///home/bgzocg/demo/tasks/cms/upload/");
        // NOTE: unix path via: https://stackoverflow.com/questions/27538608
    }
}
