package sProxy.VideoLoading;

import java.util.HashMap;

/* File Name: ThirdPartyClass
 * Author: bGZo
 * Created Time: 10/20/2022 12:25
 * License: MIT
 * Description:
 */
public class ThirdPartyClass implements ThirdPartyLib{

    @Override
    public HashMap<String, Video> popularVideos() {
        connectToServer("http://www.youtube.com");
        return getRandomVideos();
    }


    @Override
    public Video getVideo(String videoId) {
        connectToServer("http://www.youtube.com/?v=" + videoId);
        return getSomeVideo(videoId);
    }

    // Fake methods
    private void connectToServer(String server) {
        System.out.print("Connecting to " + server + "... ");
        experienceNetworkLatency();
        System.out.print("Connected!" + "\n");
    }

    private HashMap<String, Video> getRandomVideos() {
        System.out.print("Downloading populars... ");

        experienceNetworkLatency();
        HashMap<String, Video> hmap = new HashMap<String, Video>();
        hmap.put("catzzzzzzzzz", new Video("sadgahasgdas", "Catzzzz.avi"));
        hmap.put("mkafksangasj", new Video("mkafksangasj", "Dog play with ball.mp4"));
        hmap.put("dancesvideoo", new Video("asdfas3ffasd", "Dancing video.mpq"));
        hmap.put("dlsdk5jfslaf", new Video("dlsdk5jfslaf", "Barcelona vs RealM.mov"));
        hmap.put("3sdfgsd1j333", new Video("3sdfgsd1j333", "Programing lesson#1.avi"));

        System.out.print("Done!" + "\n");
        return hmap;
    }

    private void experienceNetworkLatency() {
        int randomLantency = random(5, 10);
        for (int i = 0; i < randomLantency; i++) {
            try{
                Thread.sleep(100);
            } catch (InterruptedException ex) {
                ex.printStackTrace();
            }
        }
    }

    private int random(int min, int max) {
        return (int) (min + Math.random()*( max-min + 1));
    }

    private Video getSomeVideo(String videoId) {
        System.out.print("Downloading video... ");

        experienceNetworkLatency();
        Video video = new Video(videoId, "Some video title");

        System.out.print("Done!" + "\n");
        return video;
    }

}
