package test._0526;
/* File Name: ${NAME}
 * Author: bGZo
 * Created Time: 5/30/2022 08:43
 * License: MIT
 * Description:
 */

//import jakarta.*
import jakarta.servlet.*;
import javax.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

import java.io.PrintWriter;
import java.io.IOException;

//@WebServlet(name = "testServlet", value = "/testServlet")
public class testServlet extends HttpServlet {
    private String msg;


    public void init() throws ServletException{
//        msg = "Hello testServlet!";
        msg = "Hello World , Nect To Meet You: " + System.currentTimeMillis();
        System.out.println("servlet初始化……");
        super.init();
    }


    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");

        PrintWriter out = response.getWriter();
        out.println("<h1>" + msg + "/<h1>");

        destroy();
    }

    public void destroy(){
        System.out.println("servlet销毁！");
        super.destroy();
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        super.doPost(request, response);
    }
}
