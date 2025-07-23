package cAbstractFactory;

/* File Name: AbstractFactory
 * Author: bGZo
 * Created Time: 6/21/2022 23:59
 * License: MIT
 * Description:
 */
public interface AbstractFactory {

    LowClassUnit createLowClass();

    MidClassUnit createMidClass();

    HighClassUnit createHighClass();
}
