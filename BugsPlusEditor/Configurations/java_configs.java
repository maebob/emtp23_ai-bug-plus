/*
 * MIT License
 *
 * Bug+ Interpreter
 * Copyright (c) 2022 Christian Bartelt
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package de.bugplus.examples.development;

import de.bugplus.development.*;
import de.bugplus.specification.BugplusLibrary;
import de.bugplus.specification.BugplusProgramSpecification;

/**
 * @Author Christian Bartelt
 * @Date 27.01.22 21:59
 * @Version 0.0.1
 */
public class BugplusBasicArithmetic {

    public static void main(String[] args){


        //Initialization of a new function library

        BugplusLibrary myFunctionLibrary = BugplusLibrary.getInstance();

        BugplusADDImplementation addImpl = BugplusADDImplementation.getInstance();

        myFunctionLibrary.addSpecification(addImpl.getSpecification());





        // Design of a basic incrementer

        BugplusProgramSpecification incrementSpec = BugplusProgramSpecification.getInstance("++", 1, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(incrementSpec);

        BugplusProgramImplementation incrementProgram = incrementSpec.addImplementation();

        incrementProgram.addBug("+", "0_001");

        incrementProgram.addBug("+", "1_001");
        incrementProgram.addDataFlow("0_001", "1_001", 0);

        incrementProgram.addBug("+", "+_001");

        incrementProgram.addDataFlow("1_001","+_001", 1);
        incrementProgram.addControlFlow("1_001",1,"+_001");

        incrementProgram.connectControlInInterface("1_001");
        incrementProgram.connectControlOutInterface("+_001", 0, 0);
        incrementProgram.connectControlOutInterface("+_001", 1, 1);
        incrementProgram.connectDataInInterface("+_001", 0, 0);
        incrementProgram.connectDataOutInterface("+_001");


        //Design of a basic decrementer

        BugplusProgramSpecification decrementSpec = BugplusProgramSpecification.getInstance("--", 1, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(decrementSpec);

        BugplusProgramImplementation decrementProgram = decrementSpec.addImplementation();

        decrementProgram.addBug("+", "0_001");

        decrementProgram.addBug("+", "-1_001");
        decrementProgram.addDataFlow("0_001", "-1_001", 1);

        decrementProgram.addBug("+", "+_001");
        decrementProgram.addDataFlow("-1_001","+_001", 1);
        decrementProgram.addControlFlow("-1_001",1,"+_001");

        decrementProgram.connectControlInInterface("-1_001");
        decrementProgram.connectControlOutInterface("+_001", 0, 0);
        decrementProgram.connectControlOutInterface("+_001", 1, 1);
        decrementProgram.connectDataInInterface("+_001", 0, 0);
        decrementProgram.connectDataOutInterface("+_001");


        //Design of an assignment

        BugplusProgramSpecification assignmentSpec = BugplusProgramSpecification.getInstance(":=", 1, 1, myFunctionLibrary);
        myFunctionLibrary.addSpecification(assignmentSpec);

        BugplusProgramImplementation assignmentProgram = assignmentSpec.addImplementation();

        assignmentProgram.addBug("+", "0_001");

        assignmentProgram.addBug("+", "+_001");
        assignmentProgram.addDataFlow("0_001", "+_001", 1);

        assignmentProgram.connectControlInInterface("+_001");
        assignmentProgram.connectControlOutInterface("+_001", 0, 0);
        assignmentProgram.connectControlOutInterface("+_001", 1, 0);
        assignmentProgram.connectDataInInterface("+_001", 0, 0);
        assignmentProgram.connectDataOutInterface("+_001");


        //Design of an increment iterator

        BugplusProgramSpecification iteratorSpec = BugplusProgramSpecification.getInstance("+++", 1, 1, myFunctionLibrary);
        myFunctionLibrary.addSpecification(iteratorSpec);

        BugplusProgramImplementation iteratorProgram = iteratorSpec.addImplementation();

        iteratorProgram.addBug("+", "0_001");
        iteratorProgram.addBug("+", "1_001");
        iteratorProgram.addBug("+", "+_001");

        iteratorProgram.addDataFlow("0_001", "1_001", 0);
        iteratorProgram.addDataFlow("1_001","+_001", 0);
        iteratorProgram.addDataFlow("+_001","+_001", 1);

        iteratorProgram.addControlFlow("1_001",1,"+_001");

        iteratorProgram.connectControlInInterface("1_001");
        iteratorProgram.connectControlOutInterface("+_001", 0, 0);
        iteratorProgram.connectControlOutInterface("+_001", 1, 0);

        iteratorProgram.connectDataInInterface("+_001", 1, 0);
        iteratorProgram.connectDataOutInterface("+_001");


        //Design of a decrement iterator

        BugplusProgramSpecification negIteratorSpec = BugplusProgramSpecification.getInstance("---", 1, 1, myFunctionLibrary);
        myFunctionLibrary.addSpecification(negIteratorSpec);

        BugplusProgramImplementation negIteratorProgram = negIteratorSpec.addImplementation();

        negIteratorProgram.addBug("+", "0_001");

        negIteratorProgram.addBug("+", "1_001");
        negIteratorProgram.addDataFlow("0_001", "1_001", 1);

        negIteratorProgram.addBug("+", "+_001");
        negIteratorProgram.addDataFlow("1_001","+_001", 0);
        negIteratorProgram.addDataFlow("+_001","+_001", 1);
        negIteratorProgram.addControlFlow("1_001",1,"+_001");

        negIteratorProgram.connectControlInInterface("1_001");
        negIteratorProgram.connectControlOutInterface("+_001", 0, 0);
        negIteratorProgram.connectControlOutInterface("+_001", 1, 0);
        negIteratorProgram.connectDataInInterface("+_001", 1, 0);
        negIteratorProgram.connectDataOutInterface("+_001");



        //Design an isZero-Operation

        BugplusProgramSpecification isZeroSpec = BugplusProgramSpecification.getInstance("==0", 1, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(isZeroSpec);

        BugplusProgramImplementation isZeroProgram = isZeroSpec.addImplementation();

        isZeroProgram.addBug("+", "+_001");

        isZeroProgram.connectControlInInterface("+_001");
        isZeroProgram.connectDataInInterface("+_001", 0, 0);
        isZeroProgram.connectDataInInterface("+_001", 1, 0);
        isZeroProgram.connectControlOutInterface("+_001", 0, 1);
        isZeroProgram.connectControlOutInterface("+_001", 1, 0);


        //Design a pseudo-parallel-Operation

        BugplusProgramSpecification pseudoParallelSpec = BugplusProgramSpecification.getInstance("||", 0, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(pseudoParallelSpec);

        BugplusProgramImplementation pseudoParallelProgram = pseudoParallelSpec.addImplementation();

        pseudoParallelProgram.addBug("+", "+_001");
        pseudoParallelProgram.addBug("++", "++_001");
        pseudoParallelProgram.addBug("--", "--_001");
        pseudoParallelProgram.addBug("+", "0_001");


        pseudoParallelProgram.addControlFlow("+_001", 0, "++_001");
        pseudoParallelProgram.addControlFlow("+_001", 1, "--_001");

        pseudoParallelProgram.addDataFlow("0_001", "+_001", 0);
        pseudoParallelProgram.addDataFlow("++_001", "+_001", 1);
        pseudoParallelProgram.addDataFlow("--_001", "++_001", 0);
        pseudoParallelProgram.addDataFlow("--_001", "+_001", 1);
        pseudoParallelProgram.addDataFlow("++_001", "--_001", 0);


        pseudoParallelProgram.connectControlInInterface("+_001");
        pseudoParallelProgram.connectControlOutInterface("++_001", 0, 0);
        pseudoParallelProgram.connectControlOutInterface("++_001", 1, 0);
        pseudoParallelProgram.connectControlOutInterface("--_001", 0, 1);
        pseudoParallelProgram.connectControlOutInterface("--_001", 1, 1);


        //Design an isPositive-Operation

        BugplusProgramSpecification isPositiveSpec = BugplusProgramSpecification.getInstance("?+", 1, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(isPositiveSpec);

        BugplusProgramImplementation isPositiveProgram = isPositiveSpec.addImplementation();

        isPositiveProgram.addBug("+", "0_001");
        isPositiveProgram.addBug("+", "1_001");
        isPositiveProgram.addBug("==0", "==0_001");
        isPositiveProgram.addBug(":=", ":=_001");
        isPositiveProgram.addBug(":=", ":=_002");
        isPositiveProgram.addBug(":=", ":=_003");
        isPositiveProgram.addBug(":=", ":=_004");
        isPositiveProgram.addBug(":=", ":=_005");
        isPositiveProgram.addBug("--", "--_001");
        isPositiveProgram.addBug("++", "++_001"); 
        isPositiveProgram.addBug("||", "||_001");


        isPositiveProgram.addControlFlow("1_001",1,"==0_001");
        isPositiveProgram.addControlFlow("==0_001",1, ":=_001");
        isPositiveProgram.addControlFlow("==0_001", 0, ":=_002");
        isPositiveProgram.addControlFlow(":=_002", 0, ":=_003");
        isPositiveProgram.addControlFlow(":=_003", 0, "||_001");
        isPositiveProgram.addControlFlow("||_001", 0, "++_001");
        isPositiveProgram.addControlFlow("||_001", 1, "--_001");
        isPositiveProgram.addControlFlow("++_001", 0, ":=_004");
        isPositiveProgram.addControlFlow("++_001", 1, "||_001");
        isPositiveProgram.addControlFlow("--_001", 0, ":=_005");
        isPositiveProgram.addControlFlow("--_001", 1, "||_001");


        isPositiveProgram.addDataFlow(":=_002","++_001",0);
        isPositiveProgram.addDataFlow("++_001","++_001",0);
        isPositiveProgram.addDataFlow("1_001", ":=_001", 0);
        isPositiveProgram.addDataFlow(":=_003","--_001",0);
        isPositiveProgram.addDataFlow("--_001","--_001",0);
        isPositiveProgram.addDataFlow("0_001", "1_001", 0);
        isPositiveProgram.addDataFlow("0_001", ":=_004", 0);
        isPositiveProgram.addDataFlow("1_001", ":=_005", 0);

        isPositiveProgram.connectControlInInterface("1_001");

        isPositiveProgram.connectControlOutInterface(":=_001", 0, 0);
        isPositiveProgram.connectControlOutInterface(":=_004", 0, 0);
        isPositiveProgram.connectControlOutInterface(":=_005", 0, 1);

        isPositiveProgram.connectDataInInterface("==0_001", 0, 0);
        isPositiveProgram.connectDataInInterface(":=_002", 0, 0);
        isPositiveProgram.connectDataInInterface(":=_003", 0, 0);
        
        isPositiveProgram.connectDataOutInterface(":=_001");
        isPositiveProgram.connectDataOutInterface(":=_004");
        isPositiveProgram.connectDataOutInterface(":=_005");

        


        //Design an Change-Sign-Operation

        BugplusProgramSpecification changeSignSpec = BugplusProgramSpecification.getInstance("-x", 1, 1, myFunctionLibrary);
        myFunctionLibrary.addSpecification(changeSignSpec);

        BugplusProgramImplementation changeSignProgram = changeSignSpec.addImplementation();


        changeSignProgram.addBug("+", "0_001");
        changeSignProgram.addBug("==0", "==0_001");
        changeSignProgram.addBug(":=", ":=_001");
        changeSignProgram.addBug(":=", ":=_004");
        changeSignProgram.addBug("?+", "?+_001");
        changeSignProgram.addBug(":=", ":=_002");
        changeSignProgram.addBug(":=", ":=_003");
        changeSignProgram.addBug("+++", "+++_001");
        changeSignProgram.addBug("---", "---_001");
        changeSignProgram.addBug("++", "++_001");
        changeSignProgram.addBug("--", "--_001");


        changeSignProgram.addControlFlow("++_001", 1, "+++_001");
        changeSignProgram.addControlFlow("--_001", 1, "---_001");
        changeSignProgram.addControlFlow("==0_001", 1, ":=_001");
        changeSignProgram.addControlFlow("==0_001", 0, ":=_004");
        changeSignProgram.addControlFlow(":=_004", 0, "?+_001");
        changeSignProgram.addControlFlow("?+_001", 0,":=_002");
        changeSignProgram.addControlFlow("?+_001", 1, ":=_003");
        changeSignProgram.addControlFlow(":=_002", 0, "+++_001");
        changeSignProgram.addControlFlow(":=_003", 0, "---_001");
        changeSignProgram.addControlFlow("+++_001", 0, "++_001");
        changeSignProgram.addControlFlow("---_001", 0, "--_001");


        changeSignProgram.addDataFlow("0_001", ":=_004", 0);
        changeSignProgram.addDataFlow(":=_004", "+++_001", 0);
        changeSignProgram.addDataFlow(":=_004", "---_001", 0);
        changeSignProgram.addDataFlow(":=_002", "++_001", 0);
        changeSignProgram.addDataFlow("++_001", "++_001", 0);
        changeSignProgram.addDataFlow(":=_003", "--_001", 0);
        changeSignProgram.addDataFlow("--_001", "--_001", 0);

        changeSignProgram.connectControlInInterface("==0_001");

        changeSignProgram.connectControlOutInterface(":=_001", 0, 0);
        changeSignProgram.connectControlOutInterface("++_001", 0, 0);
        changeSignProgram.connectControlOutInterface("--_001", 0, 0);


        changeSignProgram.connectDataInInterface("==0_001", 0, 0);
        changeSignProgram.connectDataInInterface("?+_001", 0, 0);
        changeSignProgram.connectDataInInterface(":=_001", 0,0 );
        changeSignProgram.connectDataInInterface(":=_002", 0, 0);
        changeSignProgram.connectDataInInterface(":=_003", 0,0);

        changeSignProgram.connectDataOutInterface(":=_001");
        changeSignProgram.connectDataOutInterface("+++_001");
        changeSignProgram.connectDataOutInterface("---_001");


        //Design a Minus-Operation

        BugplusProgramSpecification minusSpec = BugplusProgramSpecification.getInstance("-", 2, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(minusSpec);

        BugplusProgramImplementation minusProgram = minusSpec.addImplementation();

        minusProgram.addBug("-x", "-x_001");
        minusProgram.addBug("+", "+_001");

        minusProgram.addControlFlow("-x_001", 0, "+_001");
        minusProgram.addDataFlow("-x_001", "+_001", 1);

        minusProgram.connectControlInInterface("-x_001");
        minusProgram.connectControlOutInterface("+_001", 0, 0);
        minusProgram.connectControlOutInterface("+_001", 1, 1);

        minusProgram.connectDataInInterface("+_001", 0, 0);
        minusProgram.connectDataInInterface("-x_001", 0, 1);
        minusProgram.connectDataOutInterface("+_001");



        //Design a Compare-Operation

        BugplusProgramSpecification compareSpec = BugplusProgramSpecification.getInstance("==", 2, 2, myFunctionLibrary);
        myFunctionLibrary.addSpecification(compareSpec);

        BugplusProgramImplementation compareProgram = compareSpec.addImplementation();

        compareProgram.addBug("+", "0_001");
        compareProgram.addBug("+", "1_001");
        compareProgram.addBug("-", "-_001");
        compareProgram.addBug(":=", ":=_001");
        compareProgram.addBug(":=", ":=_002");

        compareProgram.addControlFlow("1_001", 1, "-_001");
        compareProgram.addControlFlow("-_001", 0, ":=_001");
        compareProgram.addControlFlow("-_001", 1, ":=_002");        

        compareProgram.addDataFlow("1_001", ":=_001", 0);
        compareProgram.addDataFlow("0_001", ":=_002", 0);
        compareProgram.addDataFlow("0_001", "1_001", 0);

        compareProgram.connectControlInInterface("1_001");
        compareProgram.connectControlOutInterface(":=_002", 0, 0);
        compareProgram.connectControlOutInterface(":=_001", 0, 1);

        compareProgram.connectDataInInterface("-_001", 0, 0);
        compareProgram.connectDataInInterface("-_001", 1, 1);
        compareProgram.connectDataOutInterface(":=_001");
        compareProgram.connectDataOutInterface(":=_002");


        //Design a Multiply-Operation

        BugplusProgramSpecification multiplySpec = BugplusProgramSpecification.getInstance("*", 2, 1, myFunctionLibrary);
        myFunctionLibrary.addSpecification(multiplySpec);

        BugplusProgramImplementation multiplyProgram = multiplySpec.addImplementation();



        multiplyProgram.addBug("+", "0_001");
        multiplyProgram.addBug("+", "0_002");
        multiplyProgram.addBug("+", "0_003");
        multiplyProgram.addBug("==", "==_001");
        multiplyProgram.addBug(":=", ":=_001");
        multiplyProgram.addBug("==", "==_002");
        multiplyProgram.addBug("+", "+_001");
        multiplyProgram.addBug("+++", "+++_001");

        multiplyProgram.addControlFlow("0_001", 0, "0_002");
        multiplyProgram.addControlFlow("0_002", 0, "0_003");
        multiplyProgram.addControlFlow("0_003", 0, "==_001");

        
        multiplyProgram.addControlFlow("==_001", 1, ":=_001");
        multiplyProgram.addControlFlow("==_001", 0, "==_002");
        multiplyProgram.addControlFlow("==_002", 1, ":=_001");
        multiplyProgram.addControlFlow("==_002", 0, "+_001");
        multiplyProgram.addControlFlow("+_001", 1, "+++_001");       
        multiplyProgram.addControlFlow("+++_001", 0, "==_001");

        multiplyProgram.addDataFlow("0_001", "==_001", 1);
        multiplyProgram.addDataFlow("0_002", ":=_001", 0);
        multiplyProgram.addDataFlow("0_003", "==_002", 1);
        multiplyProgram.addDataFlow("0_002", "+_001", 1);
        multiplyProgram.addDataFlow("0_001", "+++_001", 0);
        multiplyProgram.addDataFlow("+_001", ":=_001", 0);
        multiplyProgram.addDataFlow("+_001", "+_001", 1);
        multiplyProgram.addDataFlow("+++_001", "==_001", 1);


        multiplyProgram.connectControlInInterface("0_001");
        multiplyProgram.connectControlOutInterface(":=_001", 0, 0);

        multiplyProgram.connectDataInInterface("==_001", 0, 0);
        multiplyProgram.connectDataInInterface("==_002", 0, 1);
        multiplyProgram.connectDataInInterface("+_001", 0, 1);
        multiplyProgram.connectDataOutInterface(":=_001");



        //Application of the isZero-operation which is available in the library

        BugplusProgramSpecification isZeroTestSpec = BugplusProgramSpecification.getInstance("==0_Test", 3, 1, myFunctionLibrary);
        BugplusProgramImplementation isZeroTestImpl = isZeroTestSpec.addImplementation();

        isZeroTestImpl.addBug(":=", ":=_001");
        isZeroTestImpl.addBug(":=", ":=_002");
        isZeroTestImpl.addBug("==0", "==0_001");

        isZeroTestImpl.addControlFlow("==0_001",0,":=_001");
        isZeroTestImpl.addControlFlow("==0_001",1,":=_002");

        isZeroTestImpl.connectControlInInterface("==0_001");
        isZeroTestImpl.connectDataInInterface("==0_001", 0, 0);
        isZeroTestImpl.connectDataInInterface(":=_001", 0, 1);
        isZeroTestImpl.connectDataInInterface(":=_002", 0, 2);
        isZeroTestImpl.connectDataOutInterface(":=_001");
        isZeroTestImpl.connectDataOutInterface(":=_002");
        isZeroTestImpl.connectControlOutInterface(":=_001",0,0);
        isZeroTestImpl.connectControlOutInterface(":=_002",0,0);



// Application

        //BugplusInstance testInstance = multiplyProgram.instantiate();
        BugplusInstance testInstance = multiplyProgram.instantiateDebug();


       testInstance.setInputValue(0,4);
       testInstance.setInputValue(1,9);
        //testInstance.setInputValue(2,53);



        BugplusThread newThread = BugplusThread.getInstance();
        newThread.connectInstance(testInstance);



        newThread.start();
        System.out.println("Hier das Ergebnis: " + testInstance.getOutputValue());

  //      testInstance.setInputValue(0,-6);

        newThread.start();
        System.out.println("Hier das Ergebnis: " + testInstance.getOutputValue());

 //       testInstance.setInputValue(0,-1);

        newThread.start();
        System.out.println("Hier das Ergebnis: " + testInstance.getOutputValue());

   //     testInstance.setInputValue(0,23);

        newThread.start();
        System.out.println("Hier das Ergebnis: " + testInstance.getOutputValue());


    }
}
