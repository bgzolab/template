package sProxy.VideoLoading;

/* File Name: DemoClient
 * Author: bGZo
 * Created Time: 10/20/2022 12:47
* License: MIT
* Description:
 */
public class DemoClient {
    public static void main(String[] args) {
        Downloader naiveDownloader = new Downloader(new ThirdPartyClass());
        Downloader smartDownloader = new Downloader(new CacheProxy());

        long naive = test(naiveDownloader);
        long smart = test(smartDownloader);

        System.out.print("Time saved by caching proxy: " + (naive - smart) + "ms");
    }

    public static long test(Downloader downloader){
        long startTime = System.currentTimeMillis();

        downloader.renderPopularVideos();
        downloader.renderVideoPage("catzzzzzzzzz");
        downloader.renderPopularVideos();
        downloader.renderVideoPage("dancesvideoo");

        // Users might visit the same page quite often.
        downloader.renderVideoPage("catzzzzzzzzz");
        downloader.renderVideoPage("someothervid");

        long estimatedTime = System.currentTimeMillis() - startTime;
        System.out.print("Time elapsed: " + estimatedTime + "ms\n");
        return estimatedTime;
    }
}
