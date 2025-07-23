package cc.bgzo.cms.vo;

import lombok.Data;


/**
 *  * @Description:响应结果对象
 */
@Data
public class ResponseResult {
    private String code;   //提示码
    private String message;//提示信息

    public ResponseResult(String code, String message) {
        this.code = code;
        this.message = message;
    }
}
