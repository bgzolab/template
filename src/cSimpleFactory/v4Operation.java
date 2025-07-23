package cSimpleFactory;

public class v4Operation {
    private double _numberA = 0;
    private double _numberB = 0;

    public double getNumberA(){
        return _numberA;
    }
    public void setNumberA(double value){
        _numberA=value;
    }
    public double getNumberB(){
        return _numberB;
    }
    public void setNumberB(double value){
        _numberB=value;
    }

    public double getResult() throws Exception {
        double result = 0;
        return result;
    }
}

class OperationAdd extends v4Operation{
    public double getResult(){
        double result=0;
        result = getNumberA() + getNumberB();
        return result;
    }
}

class OperationSub extends v4Operation{
    public double getResult(){
        double result=0;
        result = getNumberA() - getNumberB();
        return result;
    }
}

class OperationMul extends v4Operation{
    public double getResult(){
        double result=0;
        result = getNumberA() * getNumberB();
        return result;
    }
}

class OperationDiv extends v4Operation{
    public double getResult() throws Exception {
        double result=0;
        if(getNumberB() == 0)
            throw new Exception("Divisor is illegal");
        result = getNumberA() / getNumberB();
        return result;
    }
}