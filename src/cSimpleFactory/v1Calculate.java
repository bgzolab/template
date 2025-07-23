package cSimpleFactory;

import java.util.Scanner;

public class v1Calculate {
    public static void main(String[] args){
        System.out.println("Number A:");
        Scanner sc= new Scanner(System.in);
        int A = sc.nextInt();
        System.out.println("+ \\ - \\ * \\ /" );
        char C = sc.next().charAt(0);
        System.out.println("Number B:");
        int B = sc.nextInt();
        String D="";

        if(C=='+')
            D = String.valueOf( A + B) ;
        if(C=='-')
            D = String.valueOf( A - B) ;
        if(C=='*')
            D = String.valueOf( A * B) ;
        if(C=='/')
            D = String.valueOf( A / B) ;

        System.out.println("Output: " + D);
    }
}
