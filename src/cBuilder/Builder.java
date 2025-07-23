package cBuilder;

/* File Name: Builder
 * Author: bGZo
 * Created Time: 6/21/2022 18:48
 * License: MIT
 * Description:
 */
public interface Builder {

    public void buildBasement();

    public void buildWall();

    public void buildRoof();

    public Building getBuilding();
}
