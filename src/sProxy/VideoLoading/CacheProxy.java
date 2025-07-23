package sProxy.VideoLoading;

import java.util.HashMap;

/* File Name: CacheProxy
 * Author: bGZo
 * Created Time: 10/20/2022 12:23
 * License: MIT
 * Description:
 */
public class CacheProxy implements ThirdPartyLib{
    private ThirdPartyLib videoService;
    private HashMap<String, Video> cachePopular = new HashMap<>();
    private HashMap<String, Video> cacheAll = new HashMap<>();

    public CacheProxy() {
        this.videoService = new ThirdPartyClass();
    }

    @Override
    public HashMap<String, Video> popularVideos() {
        if (cachePopular.isEmpty()){
            cachePopular = videoService.popularVideos();
        }else {
            System.out.println("Retrieved list from cache.");
        }
        return cachePopular;
    }

    @Override
    public Video getVideo(String videoId) {
        Video video = cacheAll.get(videoId);
        if(video == null){
            video = videoService.getVideo(videoId);
            cacheAll.put(videoId, video);
        }else{
            System.out.println("Retrieved video '" + videoId + "' from cache.");
        }
        return video;
    }

    public void reset(){
        cachePopular.clear();
        cacheAll.clear();
    }
}
