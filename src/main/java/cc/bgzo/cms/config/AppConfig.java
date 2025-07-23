package cc.bgzo.cms.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 *  */

@Data
@Component
@ConfigurationProperties(prefix = "system")
public class AppConfig {
    /**
     * 文件存储路径 + 文件访问路径
     */
    private String filePath;
    private String urlPath;
}
