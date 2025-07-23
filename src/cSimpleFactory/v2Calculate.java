package cSimpleFactory;

import java.util.Scanner;

public class v2Calculate {
    public static void main(String[] args){
        try{
            System.out.println("Number A:");
            Scanner sc= new Scanner(System.in);
            int A = sc.nextInt();
            System.out.println("+, -, *, /" );
            char C = sc.next().charAt(0);
            System.out.println("Number B:");
            int B = sc.nextInt();
            String D="";

            switch (C){
                case '+':
                    D = String.valueOf( A + B) ;
                    break;
                case '-':
                    D = String.valueOf( A - B) ;
                    break;
                case '*':
                    D = String.valueOf( A * B) ;
                    break;
                case '/':
                    if(B != 0){
                        D = String.valueOf( A / B) ;
                    } else
                        D = "除数不为0";
                    break;
            }
            System.out.println("Output: " + D);

        }catch (Exception ex){
            System.out.println("Input Error!");
        }

    }
}
