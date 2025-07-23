package cc.bgzo.cms.back.web;

import cc.bgzo.cms.config.AppConfig;
import cc.bgzo.cms.vo.FileResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 *  */

@RestController
@RequestMapping("/a/upload")
public class UploadFileController {
    @Autowired
    private AppConfig appConfig;

    @RequestMapping("/file")
    public FileResult fileUpload(MultipartFile file) {
        String fileName = "";
        if (!file.isEmpty()) {
            /**
             * 获取文件的后缀, 构造新文件的名字(时间戳), 定义文件存储的最终路径
             */
            String suffix = file.getOriginalFilename()
                    .substring(file.getOriginalFilename().lastIndexOf("."));
            fileName = System.currentTimeMillis() + suffix;
            String savePath = appConfig.getFilePath() + "/film/"+ fileName;

            File dest = new File(savePath);
            if(!dest.getParentFile().exists()) {
                dest.getParentFile().mkdirs();
            }
            try {
                file.transferTo(dest);// 保存文件
            } catch (IOException e) {
                e.printStackTrace();
                return new FileResult("300","文件上传失败");
            }
        } else {
            return new FileResult("300","文件上传失败");
        }

        String fileVisitPath = appConfig.getUrlPath() + "/public/film/" + fileName;
        String filePath = fileName;

        /**
         * 1. 前端回调地址; 2. 存表名称
         */
        List<String> list = new ArrayList<>();
        list.add(fileVisitPath);
        list.add(filePath);

        return new FileResult("200",list);
    }
}
