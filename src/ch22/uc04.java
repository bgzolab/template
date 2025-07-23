package ch22;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/* File Name: test
 * Author: @bGZo
 * Created Time: 4/27/2022 23:38
 * License: MIT
 * Description:
 */
public class test extends JFrame{

    private JButton
            b1 = new JButton("Button1"),
            b2 = new JButton("Button2");
    private JTextField txt = new JTextField(10);
//    class ButtonListener implements ActionListener{
//
//        @Override
//        public void actionPerformed(ActionEvent actionEvent) {
//            String name = ((JButton)actionEvent.getSource()).getText();
//            txt.setText(name);
//        }
//    }
    private ActionListener bl = new ActionListener(){
        @Override
        public void actionPerformed(ActionEvent actionEvent) {
            String name = ((JButton)actionEvent.getSource()).getText();
            txt.setText(name);
        }
    };//ButtonListener();

    public test(){
        b1.addActionListener(bl);
        b2.addActionListener(bl);
        setLayout(new FlowLayout());
        add(b1);
        add(b2);
        add(txt);
    }

    public static void main(String[] args) {
        uc02_01.run(new test(), 200, 100);
    }
}
