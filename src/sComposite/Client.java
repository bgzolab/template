package sComposite;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/23/2022 13:27
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        Node driveD = new Folder("D Disk");

        Node doc = new Folder("Documents");
        doc.add(new File("CV"));
        doc.add(new File("Introduce.PPT"));

        driveD.add(doc);

        Node musics = new Folder("Musics");

        Node jay = new Folder("周杰伦");
        jay.add(new File("双截棍.mp3"));
        jay.add(new File("告白气球.mp3"));
        jay.add(new File("听妈妈的话.mp3"));

        Node jack = new Folder("张学友");
        jack.add(new File("吻别.mp3"));
        jack.add(new File("一千个伤心的理由.mp3"));

        musics.add(jay);
        musics.add(jack);

        driveD.add(musics);

        driveD.tree();
    }
}
