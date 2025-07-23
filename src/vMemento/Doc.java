package vMemento;

/* File Name: Doc
 * Author: bGZo
 * Created Time: 6/23/2022 18:59
 * License: MIT
 * Description:
 */
public class Doc {
    private String title;
    private String body;

    public Doc(String title){
        this.title = title;
        this.body = "";
    }

    public void setTitle(String title) {
        this.title = title;
    }
    public String getTitle() {
        return title;
    }

    public String getBody() {
        return body;
    }
    public void setBody(String body) {
        this.body = body;
    }


    public History createHistory(){
        return new History(body);
    }
    public void restoreHistory(History history){
        this.body = history.getBody();
    }

}
