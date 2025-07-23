package cSimpleFactory;

import java.util.Scanner;

public class v3Client {

    public static void main(String[] args) {
        try {
            System.out.println("Number A:");
            Scanner sc= new Scanner(System.in);
            double numberA = sc.nextDouble();

            System.out.println("+, -, *, /" );
            String strOperate = sc.next();

            System.out.println("Number B:");
            double numberB = sc.nextDouble();

            String strResult = "";

            strResult =  String.valueOf( v3Operation.getResult( numberA,
                    numberB, strOperate) );

            System.out.println("Output: " + strResult);
        } catch (Exception ex) {
            System.out.println("Input Error");
        }
    }
}
