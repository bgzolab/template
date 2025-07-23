package cSimpleFactory;

import java.util.Scanner;

public class v4Client {
    public static void main(String[] args) throws Exception {
        System.out.println("Number A:");
        Scanner sc= new Scanner(System.in);
        double numberA = sc.nextDouble();

        System.out.println("+, -, *, /" );
        String strOperate = sc.next();

        System.out.println("Number B:");
        double numberB = sc.nextDouble();


        v4Operation oper;
        oper = v4OperationFactory.v4createOperate(strOperate);
        oper.setNumberA(numberA);
        oper.setNumberB(numberB);

        double result = oper.getResult(); //NOTE: throws sync with above

        System.out.println("Out: " + result);
    }
}
