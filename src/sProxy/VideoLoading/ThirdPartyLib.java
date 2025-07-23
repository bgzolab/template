package sProxy.VideoLoading;

import java.util.HashMap;

/* File Name: ThirdPartyLib
 * Author: bGZo
 * Created Time: 10/20/2022 12:24
 * License: MIT
 * Description:
 */
public interface ThirdPartyLib {

    HashMap<String, Video> popularVideos();

    Video getVideo(String videoId);

}
