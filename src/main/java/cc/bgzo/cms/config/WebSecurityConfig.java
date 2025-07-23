package cc.bgzo.cms.config;

import cc.bgzo.cms.back.service.impl.CustomUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.session.SessionRegistry;
import org.springframework.security.core.session.SessionRegistryImpl;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

/**
 *  */

@Configuration
@EnableWebSecurity //开启spring security功能
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
//@EnableGlobalMethodSecurity(prePostEnabled = true)

    @Autowired
    SessionRegistry sessionRegistry;

    @Bean
    public SessionRegistry getSessionRegistry() {
        SessionRegistry sessionRegistry = new SessionRegistryImpl();
        return sessionRegistry;
    }

    /**
     * 在配置类中直接实例化对象
     * @return
     */
    @Bean
    UserDetailsService customUserService() {
        return new CustomUserService();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {

        /**
         * NOTE: Refused to display 'http://localhost:9000/cms/a/console'
         * in a frame because it set 'X-Frame-Options' to 'deny'.
         */
        http.headers().frameOptions().disable();


        /**
         * NOTE: 跨域的问题 (修改密码)
         */
        http.csrf().disable();

        http.authorizeRequests() // 验证请求
            .antMatchers(
                    /**
                     * 放行静态资源
                     */
                    "/assets/**",
                    "/js/**",
                    "/public/**",
                    "/front/**"
            ).permitAll()
            .antMatchers(
                    /**
                     * 放行前台路径
                     */
                    "/f/**"
            ).permitAll()
            .anyRequest().authenticated()
                /**
                 * 任何请求,登录后可以访问
                 */
            .and()
            .formLogin()
            .loginPage("/a/user/login")
                /**
                 * 登录成功默认跳转
                  */
                .defaultSuccessUrl("/a/index",true)
                /**
                 * 登录失败跳转
                 */
                .failureUrl("/a/user/login?error")
            .permitAll()
                /**
                 * 登录页面用户任意访问
                 */

            .and()
            .logout()
                .permitAll().invalidateHttpSession(true)
                /**
                 * 注销行为任意访问
                 */
            .and()
            .sessionManagement().maximumSessions(10).expiredUrl("/a/user/login");

    }

    @Autowired
    public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {

        /**
         * NOTE:    AuthenticationManagerBuilder:   前台提交过来的的数据
         *          BCryptPasswordEncoder:          使用bcrypt强哈希加密
         */
        auth.userDetailsService(customUserService())
                .passwordEncoder(new BCryptPasswordEncoder());
    }
}


//    FIXME: the method will be deprecated!
//    @Bean
//    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
//        //解决Refused to display 'http://localhost:9000/cms/a/console' in a frame because it set 'X-Frame-Options' to 'deny'.
//        http.headers().frameOptions().disable();
//        http.csrf().disable(); //解决跨域的问题
//        http
//                .authorizeRequests()    //验证请求
//                .antMatchers("/assets/**","/js/**","/public/**","/front/**").permitAll() //放行部分合法路径
//                .antMatchers("/f/**").permitAll() //放行部分合法路径
//                .anyRequest().authenticated() //任何请求,登录后可以访问
//                .and()
//                .formLogin()
//                .loginPage("/a/user/login")
//                .defaultSuccessUrl("/a/index",true) //登录成功的默认跳转路径
//                .failureUrl("/a/user/login?error") //登录失败的跳转路径
//                .permitAll() //登录页面用户任意访问
//                .and()
//                .logout().permitAll().invalidateHttpSession(true)
//                .and().sessionManagement().maximumSessions(10).expiredUrl("/a/user/login"); //注销行为任意访问
//    }