package sProxy.VideoLoading;

import java.util.HashMap;

/* File Name: Downloader
 * Author: bGZo
 * Created Time: 10/20/2022 12:44
 * License: MIT
 * Description:
 */
public class Downloader {
    private ThirdPartyLib api;

    public Downloader(ThirdPartyLib api) {
        this.api = api;
    }

    public void renderVideoPage(String videoId){
        Video video = api.getVideo(videoId);
        System.out.println("\n-------------------------------");
        System.out.println("Video page (imagine fancy HTML)");
        System.out.println("ID: " + video.id);
        System.out.println("Title: " + video.title);
        System.out.println("Video: " + video.data);
        System.out.println("-------------------------------\n");
    }

    public void renderPopularVideos() {
        HashMap<String, Video> list = api.popularVideos();
        System.out.println("\n-------------------------------");
        System.out.println("Most popular videos on YouTube (imagine fancy HTML)");
        for (Video video : list.values()) {
            System.out.println("ID: " + video.id + " / Title: " + video.title);
        }
        System.out.println("-------------------------------\n");
    }
}
