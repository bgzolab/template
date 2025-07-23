package cc.bgzo.cms.vo;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

/**
 *  */
@Data
public class FileResult {
    private String code;
    private List<String> data;

    public FileResult(String code, List<String> data) {
        this.code = code;
        this.data = data;
    }
    public FileResult(String code, String data) {
        this.code = code;
        this.data = new ArrayList<>();
        this.data.add(data);
    }
}
